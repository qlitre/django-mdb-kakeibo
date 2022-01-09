$(function() {
  $('#id_date').datepicker({
    dateFormat: 'yy-mm-dd',
    firstDay: 1,
    dayNamesMin: ["su", "mo", "tu", "we", "th", "fr", "sa"],
    monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  });
})
