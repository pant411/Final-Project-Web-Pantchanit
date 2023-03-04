$(document).ready(function () {
    $("#myTable").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
            pageLength: 6,
            lengthChange: false,
            ordering: false
        }
    ).adjust();
});
