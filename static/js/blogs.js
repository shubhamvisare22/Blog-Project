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
        url: "create/",
        method: "POST",
        data: formData,
        dataType: "json",
        success: function (data) {
          if (data.status == 1) {
            toastr.options.onShown = function () {
              window.location.assign("/blogs/profile");
            };
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

  $("#show_blog").click(function (e) {
    e.preventDefault();
    $("#createBlogForm").hide();
    $("#blogContainer").show();

    // Toggle the visibility of the blog container
    // $("#blogContainer").toggle();

    // If the container is now visible, fetch and populate the blog data using jQuery and AJAX
    if ($("#blogContainer").is(":visible")) {
      $.ajax({
        url: "show_all_blogs/",
        type: "GET",
        dataType: "json",
        success: function (data) {
          console.log(data);
          const blogTableBody = $("#blogTableBody");
          blogTableBody.empty(); // Clear existing content

          $.each(data.blogs, function (index, blog) {
            const row = $("<tr>");
            row.append($("<td>").text(index + 1));
            row.append($("<td>").text(blog.name));
            row.append($("<td>").text(blog.content));

            let dateObject = new Date(blog.created_date)
            formattedDate = dateObject.toISOString().split("T")[0];
            row.append($("<td>").text(formattedDate));
            

            const actionsCell = $("<td>");
            const updateButton = $("<button class='btn btn-success'>").text("Update");
            updateButton.click(function () {
              console.log("Update button clicked for blog ID:", blog.id);
            });

            const deleteButton = $("<button class='btn btn-danger'>").text("Delete");
            deleteButton.click(function () {
              console.log("Delete button clicked for blog ID:", blog.id);
            });

            actionsCell.append(updateButton).append(deleteButton);
            row.append(actionsCell);
            blogTableBody.append(row);
          });
        },
        error: function (error) {
          console.error("Error fetching blogs:", error);
        },
      });
    }
  });
});
