$( document ).ready(function() {
  // toggle account menu
  $( ".account-masthead .account" ).click(function() {
    $( this ).toggleClass( "active" );
  });

  // toggle login information
  $( ".login-splash .toggle a" ).click(function() {
    $( this ).parents(".info").toggleClass( "active" );
  });
});

$( document ).ready(function() {

  // set default state
  //$(".hierarchy-tree").parent("li").addClass( "open" ); // open
  $(".hierarchy-tree").addClass('collapse').parent("li").addClass( "closed" ); // closed

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

  // auto expand parents of highlighted
  $(".hierarchy-tree-top .highlighted").parents(".closed").removeClass("closed").addClass("open").children(".hierarchy-tree").removeClass("collapse");
});

this.ckan.module('linked-datasets', function (jQuery) {
  return {

    /* holds the loaded lightbox */
    modal: null,

    options: {
      /* id of the modal dialog div */
      div: null
    },

    /* Sets up the module.
     *
     * Returns nothing.
     */
    initialize: function () {
      console.log('!!!')
      jQuery.proxyAll(this, /_on/);

      this.el.on('click', this._onClick);
      this.modal = $('#' + this.options.div)
    },

    /* Displays the API info box.
     *
     * Examples
     *
     *   module.show()
     *
     * Returns nothing.
     */
    show: function () {

      if (this.modal) {
        return this.modal.modal('show');
      }
    },

    /* Hides the modal.
     *
     * Examples
     *
     *   module.hide();
     *
     * Returns nothing.
     */
    hide: function () {
      if (this.modal) {
        this.modal.modal('hide');
      }
    },

    /* Event handler for clicking on the element */
    _onClick: function (event) {
      event.preventDefault();
      this.show();
    }
  };
});
