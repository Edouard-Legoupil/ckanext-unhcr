$( document ).ready(function() {
  // toggle account menu
  $( ".account-masthead .account" ).click(function() {
    $( this ).toggleClass( "active" );
  });
});

$( document ).ready(function() {

  // set default state
  if (
    (window.location.href.indexOf('/organization/') !== -1) ||
    (window.location.href.indexOf('/data-container/') !== -1)
    ) {
    $(".hierarchy-tree").parent("li").addClass( "open" ); // open
  } else {
    $(".hierarchy-tree").addClass('collapse').parent("li").addClass( "closed" ); // closed
  }


  // add toggle button
  $( ".hierarchy-tree" ).prev().before(
    '<button class="hierarchy-toggle"><span>Expand / collapse<span></button>'
  );

  // let CSS know that this has happened
  $(".hierarchy-tree-top").addClass('has-toggle');

  // toggle on click
  $( ".hierarchy-toggle" ).click(function() {
    $( this ).siblings(".hierarchy-tree").collapse('toggle');
    $( this ).parent("li").toggleClass( "open closed" )
  });
});
