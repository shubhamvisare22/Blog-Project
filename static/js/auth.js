$(document).ready(function () {
  // Login
  $("#login_btn").click(function (e) {
    e.preventDefault();
    let username = $("#username_id").val().trim();
    let password = $("#pass_id").val().trim();
    let csrf = $("input[name=csrfmiddlewaretoken]").val();

    if (username == "") {
      toastr.error("Enter the username", "", { timeOut: 1000 });
    } else if (password == "") {
      toastr.error("Enter the password", "", { timeOut: 1000 });
    } else {
      let myData = {
        username: username,
        password: password,
        csrfmiddlewaretoken: csrf,
      };

      $.ajax({
        url: "/auth/",
        method: "POST",
        data: myData,
        dataType: "json",
        success: function (data) {
          if (data.status == 1) {
            toastr.options.onShown = function () {
              window.location.assign("profile");
            };
            toastr.success("Successfully Logged in", "", { timeOut: 1000 });
          } else {
            $("#pass_id").val("");
            toastr.error("Username or password is incorrect.", "", {
              timeOut: 1000,
            });
          }
        },
      });
    }
  });

  // Registration
  $("#register_btn").click(function (e) {
    e.preventDefault();
    const redirectUrl = "/auth/";

    let first_name = $("#first_name").val().trim();
    let last_name = $("#last_name").val().trim();
    let username = $("#username").val().trim();
    let is_author = $("#is_author").prop("checked");
    console.log("++++++++++++++++++++++++++++ is author:", is_author);
    let password = $("#password").val().trim();
    let confirm_password = $("#confirm_password").val().trim();
    let csrf = $("input[name=csrfmiddlewaretoken]").val();

    if (first_name == "") {
      toastr.error("Enter the first name", "", { timeOut: 1000 });
    } else if (last_name == "") {
      toastr.error("Enter the last name", "", { timeOut: 1000 });
    } else if (username == "") {
      toastr.error("Enter the username", "", { timeOut: 1000 });
    } else if (password == "") {
      toastr.error("Enter the password", "", { timeOut: 1000 });
    } else if (confirm_password == "") {
      toastr.error("Enter the confirm password", "", { timeOut: 1000 });
    } else if (password !== confirm_password) {
      toastr.error("Both passwords should match", "", { timeOut: 1000 });
    } else {
      let myData = {
        first_name: first_name,
        last_name: last_name,
        username: username,
        password: password,
        is_author: is_author,
        confirm_password: confirm_password,
        csrfmiddlewaretoken: csrf,
      };

      $.ajax({
        url: "register",
        method: "POST",
        data: myData,
        dataType: "json",
        success: function (data) {
          if (data.status === 1) {
            $(
              "#first_name, #last_name, #username, #password, #confirm_password",
              "#is_author"
            ).val("");
            toastr.options.onShown = function () {
              window.location.assign(redirectUrl);
            };
            toastr.success("Registered Successfully.", "", { timeOut: 1000 });
          } else {
            toastr.error("Username already exists.", "", { timeOut: 1000 });
          }
        },
      });
    }
  });

  // Logout
  $("#logout_btn").click(function (e) {
    e.preventDefault();
    let csrf = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      url: "logout",
      method: "POST",
      data: { csrfmiddlewaretoken: csrf },
      dataType: "json",
      success: function (data) {
        if (data.status === 1) {
          toastr.options.onShown = function () {
            window.location.assign("profile");
          };
          toastr.success("Logged out Successfully.", "", { timeOut: 1000 });
        }
      },
    });
  });
});
