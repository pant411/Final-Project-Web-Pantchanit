$(document).ready(function () {
    $("#myTable").DataTable(
        {
            scrollY: '72vh',
            scrollCollapse: true,
            paging: true,
            pageLength: 10,
            lengthChange: false,
            ordering: false
        }
    ).adjust();
});
