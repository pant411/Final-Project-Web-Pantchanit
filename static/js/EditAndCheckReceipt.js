const ListRemove = [];

async function submitUpdateListItem(receipt_id) {
  let thisElement =  document.getElementById("list-item-receipt-section");
  let listItem = thisElement.children;
  let ListItemUpdate = [];
  let payloadReceipt = {}

  let receiptID = document.getElementById("input-receipt-id").value
  let dateReceipt = document.getElementById("input-receipt-date").value
  let shopName = document.getElementById("input-receipt-shopname").value
  let shopPhone = document.getElementById("input-receipt-shopphone").value
  let addressShop = document.getElementById("input-receipt-addressshop").value
  let taxIDShop = document.getElementById("input-receipt-taxIDShop").value
  let customerName = document.getElementById("input-receipt-customerName").value
  let addressCust = document.getElementById("input-receipt-addressCust").value
  let taxIDCust = document.getElementById("input-receipt-taxIDCust").value
  let type_item = document.getElementById("type-item-dropdown").value;
  let type_receipt = document.getElementById("type-receipt-dropdown").value;
  if (receiptID) {
    payloadReceipt['receiptID'] = receiptID
  }
  if (dateReceipt) {
    payloadReceipt['dateReceipt'] = dateReceipt
  }
  if (shopName) {
    payloadReceipt['shopName'] = shopName
  }
  if (shopPhone) {
    payloadReceipt['shopPhone'] = shopPhone
  }
  if (addressShop) {
    payloadReceipt['addressShop'] = addressShop
  }  
  if (taxIDShop) {
    payloadReceipt['taxIDShop'] = taxIDShop
  }
  if (customerName) {
    payloadReceipt['customerName'] = customerName
  }
  if (addressCust) {
    payloadReceipt['addressCust'] = addressCust
  }
  if (taxIDCust) {
    payloadReceipt['taxIDCust'] = taxIDCust
  }
  if (type_item) {
    payloadReceipt["type_item"] = type_item
  }
  if (type_receipt) {
    payloadReceipt["type_receipt"] = type_receipt
  }
  // console.log(payloadReceipt);
  for (let ele of listItem) {
    if (ele.id === "x1") {
      continue;
    }
    let payloadItem = {};
    let id = Number(ele.id)
    let nameItem = ele.children[0].children[1].value;
    let qty = Number(ele.children[1].children[1].value);
    let unitQty = ele.children[2].children[1].value;
    let pricePerQty = Number(ele.children[3].children[1].value);
    let priceItemTotal = Number(ele.children[4].children[1].value);    
    if (type_item == 1) {

      if (id) {
        payloadItem['id'] = id
      }
      if (nameItem) {
        payloadItem['nameItem'] = nameItem
      }
      if (qty) {
        payloadItem['qty'] = qty
      }
      if (unitQty) {
        payloadItem['unitQty'] = unitQty
      }
      if (pricePerQty) {
        payloadItem['pricePerQty'] = pricePerQty
      }
      if (priceItemTotal) {
        payloadItem['priceItemTotal'] = priceItemTotal
      }      
    } else if (type_item == 0) {
      // let nameItem = ele.children[0].children[1].value;
      // let priceItemTotal = Number(ele.children[1].children[1].value);
      if (id) {
        payloadItem['id'] = id
      }
      if (nameItem) {
        payloadItem['nameItem'] = nameItem
      }
      if (priceItemTotal) {
        payloadItem['priceItemTotal'] = priceItemTotal
      }
    }
    ListItemUpdate.push(payloadItem)
  }
  // console.log(ListItemUpdate);
  // console.log(ListRemove);
  // console.log(receipt_id);
  await fetch('/receipts/editreceiptall/' + receipt_id + '/' + type_item, {
    method: 'PATCH',
    body: JSON.stringify({
      editItem: ListItemUpdate,
      deleteItem: ListRemove,
      dataReceipt: payloadReceipt
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
      'Cache-Control': 'no-cache, no-store, must-revalidate'
    },
  }).then(response => {
    if (response.ok) {
        return window.location.href = "/statusreceipts";
    } else {
        alert(response.status);
    }
})
  
}

function addListItem(type_item) {
  add_item_0 =`
  <div class="row" >
    <div class="form-group col-7">
        <label for="input-receipt-nameItem">รายการ</label>
        <input class="form-control form-control-sm" type="text" id="input-receipt-nameItem">
    </div>
    <div class="form-group col-3">
        <label for="input-receipt-priceItemTotal">ราคาทั้งหมด</label>
        <input class="form-control form-control-sm" type="text" id="input-receipt-priceItemTotal">
    </div>
    <div class="col-1" id="icon-receipt">
      <i class="fas fa-trash" id="icon-remove-item" onclick="removeListItem(this)"></i>
    </div> 
  </div>`;

  add_item_1 = `
  <div class="row" >
    <div class="form-group col-5">
        <label for="input-receipt-nameItem">รายการ</label>
        <input class="form-control form-control-sm" type="text" id="input-receipt-nameItem">
    </div>
    <div class="form-group col-1">
        <label for="input-receipt-qty">จำนวน</label>
        <input class="form-control form-control-sm" type="text" id="input-receipt-qty">
    </div>
    <div class="form-group col-1">
        <label for="input-receipt-unitQty">หน่วย</label>
        <input class="form-control form-control-sm" type="text" id="input-receipt-unitQty">
    </div>
    <div class="form-group col-2">
        <label for="input-receipt-pricePerQty">ราคาต่อหน่วย</label>
        <input class="form-control form-control-sm" type="text" id="input-receipt-pricePerQty">
    </div>
    <div class="form-group col-2">
        <label for="input-receipt-priceItemTotal">ราคาทั้งหมด</label>
        <input class="form-control form-control-sm" type="text" id="input-receipt-priceItemTotal">
    </div>
    <div class="col-1" id="icon-receipt">
      <i class="fas fa-trash" id="icon-remove-item" onclick="removeListItem(this)"></i>
    </div> 
  </div>`;

  let thisElement =  document.getElementById("list-item-receipt-section");

  if(type_item == 0) {
    thisElement.innerHTML += add_item_0;
  } else if (type_item == 1) {
    thisElement.innerHTML += add_item_1;
  }
}

function removeListItem(thisElement) {
  let parentDiv = thisElement.parentElement.parentElement;
  console.log(parentDiv.id);
  parentDiv.remove();
  ListRemove.push(parentDiv.id)
}
