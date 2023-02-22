$(document).ready(function () {
    $("#myTable-detail-1").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
            pageLength: 5,
            lengthChange: false,
            ordering: false,
            columns: [
                { width: '60%' },
                { width: '10%' },
                { width: '10%' },
                { width: '10%' },
                { width: '10%' }
            ]
        }
    ).columns.adjust().draw()

    $("#myTable-detail-2").DataTable(
        {
            scrollY: '60vh',
            scrollCollapse: true,
            paging: true,
            pageLength: 5,
            lengthChange: false,
            ordering: false,
            columns: [
                { width: '80%' },
                { width: '20%' }
            ],

        }
    ).columns.adjust().draw()

});
