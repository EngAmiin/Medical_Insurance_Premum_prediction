// Selecting form elements
const age = document.querySelector("#age");
const gender = document.querySelector("#gender");
const bmi = document.querySelector("#bmi");
const children = document.querySelector("#children");
const smoker = document.querySelector("#smoker");
const region = document.querySelector("#region");
const predictValue = document.getElementById("predictedValue");
const form = document.getElementById("userForm");

const email= document.querySelector("#email");
const password= document.querySelector("#password");

$('.login').click(()=>{
  if(email.value== ""){
    showToast("error", "Email is required please!");
    return;
  }
  if(password.value== ""){
    showToast("error", "Password is required please!");
    return;
  }
})


$('.predict').click(()=>{
  if (age.value === "") {
        showToast("error", "Age is required please!");
        return;
      }
      if (isNaN(age.value) || age.value <= 0) {
        showToast("error", "Invalid Age!");
        return;
      }
      if(isNaN(age.value) || age.value <= 18) {
        showToast("error", "Age MustBe Greater Then 18 !");
        return;
      }
      if(isNaN(age.value) || age.value >= 100) {
        showToast("error", "Age MustBe Less Then 100 !");
        return;
      }
      if (bmi.value === "") {
        showToast("error", "BMI is required please!");
        return;
      }
      if (isNaN(bmi.value) || bmi.value <= 0) {
        showToast("error", "Invalid BMI!");
        return;
      }
      if(isNaN(bmi.value) || bmi.value <=14){
        showToast("error", "BMI MustBe Greater Than 15 !");
        return;
      }
      if(isNaN(bmi.value) || bmi.value >=36){
        showToast("error", "BMI MustBe Less Than 35 !");
        return;
      }
      if (children.value === "") {
        showToast("error", "Number of Memebers is required!");
        return;
      }
      if (isNaN(children.value) || children.value <= -1) {
        showToast("error", "Invalid Members !");
        return;
      }
      if(isNaN(children.value) || children.value>=16){
        showToast("error", "NO. Of Members Must Be Lessthen 15 !");
        return;
      }
      if (gender.value === "") {
        showToast("error", "Please select your gender!");
        return;
      }
      if (smoker.value === "") {
        showToast("error", "Please select your smoking status!");
        return;
      }
      if (region.value === "") {
        showToast("error", "Please select the region!");
        return;
      }
  let data= {
    age: age.value,
    gender: gender.value,
    bmi: bmi.value,
    children: children.value,
    smoker: smoker.value,
    region: region.value,
  }
  $.ajax({
    url: 'http://127.0.0.1:5000/predict',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: function(data) {
      let respnse= JSON.parse(data.data) [
        0
      ]
      console.log(respnse);
          // Display success message
          Swal.fire({
            title: "Your Mediccal Insurance Is: $" + parseFloat(respnse).toFixed(2),
            showClass: {
              popup: `animate__animated`
            },
          });
    },
    error: function(error){
      console.log(error);
    }
  })
});

// Function to display toast message
function showToast(icon, title) {
  const Toast = Swal.mixin({
    toast: true,
    position: "top-right",
    showConfirmButton: false,
    timer: 2000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.onmouseenter = Swal.stopTimer;
      toast.onmouseleave = Swal.resumeTimer;
    }
  });
  Toast.fire({
    icon: icon,
    title: title
  });
}