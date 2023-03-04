$(document).ready(function () {
    $("#myTable-status").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
            pageLength: 8,
            lengthChange: false,
            ordering: false
        }
    ).adjust();
});
