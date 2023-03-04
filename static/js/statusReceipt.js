async function removeReceipt(receipt_id) {
    console.log(receipt_id)
    await fetch('/receipts/deleteReceiptByID/' + receipt_id , {
        method: 'DELETE',
      })
        .then((response) => response.json())
        .then((json) => console.log(json))
        .then(location.href = "/statusreceipts");
  }