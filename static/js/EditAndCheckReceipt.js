function updateReceipt(receipt_id, payload) {
    fetch('/receipts/editonereceipt/' + receipt_id, {
        method: 'PATCH',
        body: JSON.stringify(payload),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      })
        .then((response) => response.json())
        .then((json) => console.log(json));
}

function updateItemReceipt(receipt_id, item_id, payload) {
    fetch('/receipts/editoneitem/' + receipt_id + '/' + item_id, {
        method: 'PATCH',
        body: JSON.stringify(payload),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      })
        .then((response) => response.json())
        .then((json) => console.log(json));
}
