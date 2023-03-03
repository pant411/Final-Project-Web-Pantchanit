$(document).ready(function () {
    $("#myTable-status").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
        }
    ).adjust();
});
