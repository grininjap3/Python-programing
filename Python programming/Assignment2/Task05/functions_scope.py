"""Q5: Mutable defaults, parameters, returns and scope."""
def add_item_buggy(item, order=[]):
    order.append(item); return order

def add_item(item, order=None):
    if order is None: order=[]
    order.append(item); return order

def bill_with_gst(amount, gst_rate=0.05):
    gst=amount*gst_rate
    return amount+gst, gst

count=0
def global_example():
    global count
    count += 1

def make_counter():
    value=0
    def increment():
        nonlocal value
        value += 1
        return value
    return increment

if __name__ == "__main__":
    print(add_item_buggy("Tea"),add_item_buggy("Vada"))
    print(add_item("Tea"),add_item("Vada"))
    print("defaults:",add_item_buggy.__defaults__)
    print("bill:",bill_with_gst(200,gst_rate=0.05))
    counter=make_counter(); global_example()
    print("global:",count,"nonlocal:",counter(),counter())
