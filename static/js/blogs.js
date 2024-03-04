$(document).ready(function () {
  
  // create blog
  $("#create_blog_btn").click(function (e) {
    e.preventDefault();
    let name = $("#blog_name").val().trim();
    let content = $("#blog_content").val().trim();
    let csrf = $("input[name=csrfmiddlewaretoken]").val();

    // validations
    if (name == "") {
      console.log("Enter the name");
      toastr.error("Enter the name", "", { timeOut: 1000 });
    } else if (content == "") {
      console.log("Enter the content");
      toastr.error("Enter the content", "", { timeOut: 1000 });
    } else {
      let formData = {
        name: name,
        content: content,
        csrfmiddlewaretoken: csrf,
      };
      console.log(formData);
      
      $.ajax({
        url: "create-blog",
        method: "POST",
        data: formData,
        dataType: "json",
        success: function (data) {
          if (data.status == 1) {
            // toastr.options.onShown = function () {
            //   window.location.assign("profile");
            // };
            $("#blog_name").val("");
            $("#blog_content").val("");
            toastr.success("Successfully created blog", "", { timeOut: 1000 });
          } else {
            toastr.error("Something went wrong.", "", {
              timeOut: 1000,
            });
          }
        },
      });
    }
  });
});
