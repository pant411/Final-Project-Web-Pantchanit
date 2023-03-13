$(document).ready(function () {
    $("#myTable-status").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
            pageLength: 10,
            lengthChange: false,
            ordering: false
        }
    ).adjust();
});
