from django.shortcuts import render,get_object_or_404
from django_pandas.io import read_frame
# Create your views here.
from django.shortcuts import render,redirect
from inventoryapp.models import Inventory,InventoryUser
import json
import plotly
import plotly.express as px
# Create your views here.
def index(request):
    if request.session.get('InventoryUser'):
        inventories = Inventory.objects.all()
        content={'inventories':inventories}
        return render(request,'inventory/index.html',content)
    else:
        return render(request,'inventory/login.html')

def login(request):
    if request.method=='GET':
        request.session['InventoryUser']=''
        return render(request,'inventory/login.html')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if InventoryUser.objects.filter(email=email,password=password):
            request.session['InventoryUser']=list(InventoryUser.objects.filter(email=email,password=password).values())[0]['name']
            request.session['id']=list(InventoryUser.objects.filter(email=email,password=password).values())[0]['id']
            return redirect('home_inventory')
        else:
            return render(request,'inventory/login.html',{"error":"invalid Email or Password"})


def signup(request):
    if request.method=='GET':
        return render(request,'inventory/signup.html')
    if request.method=='POST':
        name = request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if InventoryUser.objects.filter(email=email):
            return render(request,'inventory/signup.html',{"error":"email already exist try sign in using different mail.!!!"})
        else:
            user=InventoryUser(name=name,email=email,password=password)
            user.save()
            return render(request,'inventory/signup.html',{"success":"user registered try login!!!"})

def logout(request):
    request.session['InventoryUser']=''
    return render(request,'inventory/login.html')
        
def update(request, id):
    if request.session.get('InventoryUser'):
        if request.method=='GET':
            inventory = get_object_or_404(Inventory, id=id)
            content={'inventory':inventory}
            return render(request,'inventory/update.html',content)
        if request.method=='POST':
            name = request.POST.get('name')
            cost_per_item=request.POST.get('costperitem')
            quantity_in_stock=request.POST.get('quantity')
            quantity_sold=request.POST.get('quantitysold')
            if isValidFloat(cost_per_item) and isValidInt(quantity_in_stock) and isValidInt(quantity_sold):
                inventory = get_object_or_404(Inventory, id=id)
                inventory.name=name
                inventory.cost_per_item=float(cost_per_item)
                inventory.quantity_in_stock=int(quantity_in_stock)
                inventory.quantity_sold=int(quantity_sold)
                inventory.sales=float(cost_per_item)*int(quantity_sold)
                inventory.save()
                return redirect('home_inventory')
            else:
                inventory = get_object_or_404(Inventory, id=id)
                content={'inventory':inventory,
                         'error': "incorrect data"}
                return render(request,'inventory/update.html',content)
            
def delete(request,id):
    if request.session.get('InventoryUser'):
        inventory = get_object_or_404(Inventory, id=id)
        inventory.delete()
        return redirect('home_inventory')



def addProduct(request):
    if request.session.get('InventoryUser'):
        if request.method=='GET':
            return render(request,'inventory/addproduct.html')
        if request.method=='POST':
            name = request.POST.get('name')
            cost_per_item=request.POST.get('costperitem')
            quantity_in_stock=request.POST.get('quantity')
            quantity_sold=request.POST.get('quantitysold')
            if isValidFloat(cost_per_item) and isValidInt(quantity_in_stock) and isValidInt(quantity_sold):
                inventory=Inventory(name=name,cost_per_item=cost_per_item,quantity_in_stock=quantity_in_stock,
                                    quantity_sold=quantity_sold,sales=(int(quantity_sold)*float(cost_per_item))
                )
                inventory.save()
                return redirect('home_inventory')
            else:
                content={'error': "incorrect data"}
                return render(request,'inventory/update.html',content)
            


def dashboard(request):
    if request.session.get('InventoryUser'):
        if Inventory.objects.count()!=0:
            inventories = Inventory.objects.all()
            df = read_frame(inventories)
            
            # sales graph
            print(df.columns)
            sales_graph_df = df.groupby(by="last_sales_date", as_index=False, sort=False)['sales'].sum()
            print(sales_graph_df.sales)
            print(sales_graph_df.columns)
            sales_graph = px.line(sales_graph_df, x = sales_graph_df.last_sales_date, y = sales_graph_df.sales, title="Sales Trend")
            sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)

            
            # best performing product
            best_performing_product_df = df.groupby(by="name").sum().sort_values(by="quantity_sold")
            best_performing_product = px.bar(best_performing_product_df, 
                                            x = best_performing_product_df.index, 
                                            y = best_performing_product_df.quantity_sold, 
                                            title="Best Performing Product"
                                        )
            best_performing_product = json.dumps(best_performing_product, cls=plotly.utils.PlotlyJSONEncoder)


            # best performing product in sales
            sales_graph_df_per_product_df = df.groupby(by="name", as_index=False, sort=False)['sales'].sum()
            best_performing_product_per_product = px.pie(sales_graph_df_per_product_df, 
                                            names = "name", 
                                            values = "sales", 
                                            title="Product Performance By Sales",
                                            # https://plotly.com/python/discrete-color/
                                            color_discrete_sequence=px.colors.qualitative.Bold,
                                        )
            best_performing_product_per_product = json.dumps(best_performing_product_per_product, cls=plotly.utils.PlotlyJSONEncoder)


            # Most Product In Stock
            most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
            most_product_in_stock = px.pie(most_product_in_stock_df, 
                                            names = most_product_in_stock_df.index, 
                                            values = most_product_in_stock_df.quantity_in_stock, 
                                            title="Most Product In Stock"
                                        )
            most_product_in_stock = json.dumps(most_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)

            context = {
                "sales_graph": sales_graph,
                "best_performing_product": best_performing_product,
                "most_product_in_stock": most_product_in_stock,
                "best_performing_product_per_product": best_performing_product_per_product
            }

            return render(request,"inventory/dashboard.html", context=context)
        else:
            return render(request,"inventory/dashboard.html")



# utility fumctions       
def isValidInt(n):
    try:
        int(n)
        return True
    except:
        return False

def isValidFloat(n):
    try:
        float(n)
        return True
    except:
        return False
        