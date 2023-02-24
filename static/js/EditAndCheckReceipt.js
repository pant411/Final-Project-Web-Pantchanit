const ListRemove = [];

async function updateItemReceipt(thisElement,receipt_id, type_receipt) {
  let parentDiv = thisElement.parentElement.parentElement;
  let item_id = parentDiv.id
  console.log(item_id);
  let nameItem = parentDiv.children[0].children[1].value;
  let payload = {} 
  if (type_receipt == 1) {
    let qty = Number(parentDiv.children[1].children[1].value);
    let unitQty = parentDiv.children[2].children[1].value;
    let pricePerQty = Number(parentDiv.children[3].children[1].value);
    let priceItemTotal = Number(parentDiv.children[4].children[1].value);
    payload = {
      nameItem: nameItem,
      qty: qty,
      unitQty: unitQty,
      pricePerQty: pricePerQty,
      priceItemTotal: priceItemTotal
    }    
  } else if (type_receipt == 0) {
    let priceItemTotal = Number(parentDiv.children[1].children[1].value);
    payload = {
      nameItem: nameItem,
      priceItemTotal: priceItemTotal
    }     
  }
  console.log(payload);
  // console.log(receipt_id);
  // console.log(type_receipt);
  // console.log(item_id);
  // console.log(item_id);
  await fetch('/receipts/editoneitem/' + receipt_id + '/' + item_id, {
    method: 'PATCH',
    body: JSON.stringify(payload),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    },
  }).then((response) => response.json())
    .then((json) => console.log(json))
    .then(location.href = "/editreceipt/"+receipt_id);
}

async function updateItemReceiptCheck(thisElement,receipt_id,type_receipt) {
  let parentDiv = thisElement.parentElement;
  let item_id = parentDiv.id
  let nameItem = parentDiv.children[0].children[1].value;
  let payload = {} 
  if (type_receipt == 1) {
    let qty = parentDiv.children[1].children[1].value;
    let unitQty = parentDiv.children[2].children[1].value;
    let pricePerQty = Number(parentDiv.children[3].children[1].value);
    let priceItemTotal = Number(parentDiv.children[4].children[1].value);
    payload = {
      nameItem: nameItem,
      qty: qty,
      unitQty: unitQty,
      pricePerQty: pricePerQty,
      priceItemTotal: priceItemTotal
    }    
  } else if (type_receipt == 0) {
    let priceItemTotal = Number(parentDiv.children[1].children[1].value);
    payload = {
      nameItem: nameItem,
      priceItemTotal: priceItemTotal
    }     
  }
  // console.log(payload);
  // console.log(receipt_id);
  // console.log(type_receipt);
  // console.log(item_id);
  // console.log(item_id);
  await fetch('/receipts/editoneitem/' + receipt_id + '/' + item_id, {
    method: 'PATCH',
    body: JSON.stringify(payload),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    },
  }).then(location.href = "/checkreceipt/"+receipt_id);
}

async function removeItemReceipt(thisElement,receipt_id) {
  let parentDiv = thisElement.parentElement;
  let item_id = parentDiv.id
  console.log(item_id)
  await fetch('/receipts/deleteitem/' + receipt_id + '/' + item_id, {
      method: 'DELETE',
    })
      .then((response) => response.json())
      .then((json) => console.log(json))
      .then(location.href = "/editreceipt/"+receipt_id);
}

async function removeItemReceiptCheck(thisElement,receipt_id) {
  let parentDiv = thisElement.parentElement;
  let item_id = parentDiv.id
  await fetch('/receipts/deleteitem/' + receipt_id + '/' + item_id, {
      method: 'DELETE',
    })
      .then((response) => response.json())
      .then((json) => console.log(json))
      .then(location.href = "/checkreceipt/"+receipt_id);
}

async function addItemReceipt(receipt_id) {
  await fetch('/receipts/editoneitem/' + receipt_id + '/' + item_id, {
      method: 'POST',
      body: JSON.stringify(payload),
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    })
      .then((response) => response.json())
      .then((json) => console.log(json));
}

function submitUpdateListItem(type_receipt) {
  let thisElement =  document.getElementById("list-item-receipt-section");
  let listItem = thisElement.children;

  let ListItemUpdate = [];

  for (let ele of listItem) {
    if (type_receipt == 1) {
      let nameItem = ele.children[0].children[1].value;
      let qty = ele.children[1].children[1].value;
      let unitQty = ele.children[2].children[1].value;
      let pricePerQty = Number(ele.children[3].children[1].value);
      let priceItemTotal = Number(ele.children[4].children[1].value);
      payload = {
        id: ele.id,
        nameItem: nameItem,
        qty: qty,
        unitQty: unitQty,
        pricePerQty: pricePerQty,
        priceItemTotal: priceItemTotal
      }  
    } else if (type_receipt == 0) {
      let nameItem = ele.children[0].children[1].value;
      let priceItemTotal = Number(ele.children[1].children[1].value);
      payload = {
        id: ele.id,
        nameItem: nameItem,
        priceItemTotal: priceItemTotal
      }  
    }
    ListItemUpdate.push(payload)
    
  }
  console.log(ListItemUpdate);
  console.log(ListRemove);
}

function addListItem(type_receipt) {
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

  if(type_receipt == 0) {
    thisElement.innerHTML += add_item_0;
  } else if (type_receipt == 1) {
    thisElement.innerHTML += add_item_1;
  }
}

function removeListItem(thisElement) {
  let parentDiv = thisElement.parentElement.parentElement;
  console.log(parentDiv.id);
  parentDiv.remove();
  ListRemove.push(parentDiv.id)
}
