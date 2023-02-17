$(document).ready(function () {
    $("#myTable").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
            pageLength: 14,
            lengthChange: false
        }
    );
});
