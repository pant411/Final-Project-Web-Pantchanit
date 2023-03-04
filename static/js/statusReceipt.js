async function removeReceipt(receipt_id) {
    console.log(receipt_id)
    await fetch('/receipts/deleteReceiptByID/' + receipt_id , {
        method: 'DELETE',
      }).then(response => {
        if (response.ok) {
            return window.location.href = "/statusreceipts";
        } else {
            return {status: response.status};
        }
    })
  }