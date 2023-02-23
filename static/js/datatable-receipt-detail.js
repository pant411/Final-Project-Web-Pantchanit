$(document).ready(function () {

    $("#myTable-detail-1").DataTable(
        {
            scrollY: '55vh',
            scrollCollapse: true,
            paging: true,
            /*pageLength: 6,
            lengthChange: false,*/
            ordering: false,
            columns: [
                { width: '60%' },
                { width: '10%' },
                { width: '10%' },
                { width: '10%' },
                { width: '10%' }
            ]
        }
    ).columns.adjust()

    $("#myTable-detail-2").DataTable(
        {
            scrollY: '55vh',
            scrollCollapse: true,
            paging: true,
            /*pageLength: 6,
            lengthChange: false,*/
            ordering: false,
            columns: [
                { width: '80%' },
                { width: '20%' }
            ],
        }
    ).columns.adjust()

    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function(e){
        $($.fn.dataTable.tables(true)).DataTable().columns.adjust()
        .responsive.recalc();
     });
    
});
