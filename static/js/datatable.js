$(document).ready(function () {
    $("#myTable").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
            order: [
                [5, "desc"]
            ],
        }
    ).adjust();
});
