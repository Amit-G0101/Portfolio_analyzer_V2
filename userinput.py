
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from dataclasses import dataclass
def get_valid_input(prompt:str,validation_func,*args):
    while True:
        try:
            return validation_func(input(prompt),*args)
        except ValueError as e:
            print(f"❌ {e}. Please try again\nRe-enter the valid value:")

def validate_string(value:str,field_name:str,max_length:int):
    if not isinstance(value,str) or len(value)>max_length:
        raise ValueError(f"{field_name} must be a string with max {max_length} characters.")
    else:
        return value.strip()

def validate_transaction_type(value:str):
    value=value.upper()
    if value not in ('BUY','SELL','BONUS'):
        raise ValueError("Transaction Type must be either 'BUY' or 'SELL' or 'BONUS' ONLY.")
    else:
        return value
    
def validate_nonzero_positive_int(value:str,field_name:str)->int:
    try:
        num=int(value)
        if num <= 0:
            raise ValueError
        return num
    except:
        raise ValueError(f"{field_name} must be a non-zero positive Integer ")
    
def validate_nonzero_positive_float(value:str,field_name:str) -> float:
    try:
        num = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if num <=0:
            raise ValueError
        return num
    except:
        raise ValueError(f"{field_name} must be a non-zero positive float ")


def validate_date(value:str):
    try:
        datetime.strptime(value,"%Y-%m-%d")
        return value
    except:
        raise ValueError("Transaction Date must be in 'YYYY-MM-DD' format.")

@dataclass
class Transaction:
    stock_id:str
    broker_id:str
    trnsc_type:str
    qty:int
    price:Decimal
    tax_charg:Decimal
    trnsc_date:str

    @property
    def total_amount(self):
        return(self.qty * self.price)


def usr_input():
    print("\n" + "="*50)
    print("🟢 Welcome to the Stock Transaction Entry Portal 🟢".center(50))
    print("="*50)
    
    stock_id=get_valid_input("📌 Enter STOCK ID (Max 30 characters): ",validate_string,"Stock Id",30)
    broker_id = get_valid_input("🏦 Enter Broker ID (Max 30 characters): ", validate_string, "Broker ID", 30)
    trnsc_type = get_valid_input("🔄 Enter Transaction Type (BUY/SELL/BONUS): ", validate_transaction_type)
    qty=get_valid_input("📊 Enter Quantity: ", validate_nonzero_positive_int," Stock Quantity")
    price = get_valid_input("💰 Enter Price at Time of Transaction: ", validate_nonzero_positive_float, "Price")
    tax_charg = get_valid_input("💸 Enter Brokerage and Tax Amount: ", validate_nonzero_positive_float, "Brokerage and Tax Amount")
    trnsc_date = get_valid_input("📅 Enter Transaction Date (YYYY-MM-DD): ", validate_date)

    trnsc_obj=Transaction(stock_id,broker_id,trnsc_type,qty,price,tax_charg,trnsc_date)
    
    # Test output Display
    # print(trnsc_obj.stock_id,trnsc_obj.broker_id,trnsc_obj.trnsc_type,trnsc_obj.qty,trnsc_obj.price,
    #       trnsc_obj.trnsc_date,trnsc_obj.total_amount,trnsc_obj.tax_charg,sep='\n')

    return trnsc_obj
    
# enable testing    
# usr_input()
