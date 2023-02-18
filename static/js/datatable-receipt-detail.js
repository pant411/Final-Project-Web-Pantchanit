$(document).ready(function () {
    $("#myTable").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
            pageLength: 5,
            lengthChange: false,
            ordering: false
        }
    );
});
