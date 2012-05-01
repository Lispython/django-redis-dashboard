;(function($) {
function commands_shell_init() {
  console.log("Commands shell init");
  $('div.shell').each(function() {
    var $shell = $(this);
    var $form = $shell.find("form");
    var $input = $form.find("input");

    $input.keydown(function(event) {
      var count = $shell.find(".command").size();
      var index = $input.data("index");
      if (index == undefined) index = count;

      if (event.keyCode == 38) {
        index--; // up
      } else if (event.keyCode == 40) {
        index++; // down
      } else {
        return;
      }

      // Out of range at the positive side of the range makes sure
      // we can get back to an empty value.
      if (index >= 0 && index <= count) {
        $input.data("index", index);
        $input.val($shell.find(".command").eq(index).text());
        $input.setSelection($input.val().length);
      }

      return false;
    });

    $form.submit(function(event) {
      if ($input.val().length == 0)
        return false;

      // Append command to execute
      var ps1 = $("<span></span>")
        .addClass("monospace")
        .addClass("prompt")
        .html("redis&gt;&nbsp;");
      var cmd = $("<span></span>")
        .addClass("monospace")
        .addClass("command")
        .text($input.val());
      $form.before(ps1);
      $form.before(cmd);

      // Hide form
      $form.hide();

      // POST command to app
      $.ajax({
        type: "post",
        url: "/session/" + $shell.attr("data-session"),
        data: $form.serialize(),
        complete: function(xhr, textStatus) {
          var data = xhr.responseText;
          var pre = $("<pre></pre>").text(data);
          $form.before(pre);

          // Reset input field and show form
          $input.val("");
          $input.removeData("index");
          $form.show();
        }
      });

      return false;
    });
  });

  // Only focus field when it is visible
  var $first = $('div.shell:first :text');
  if ($first.size() > 0) {
    var windowTop = $(window).scrollTop();
    var windowBottom = windowTop + $(window).height();
    var elemTop = $first.offset().top;
    var elemBottom = elemTop + $first.height();
    if (elemTop >= windowTop && elemBottom < windowBottom) {
      $first.focus();
    }
  }
}

$(document).ready(function() {
  commands_shell_init();
})

})(jQuery);