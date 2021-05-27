function  check()
{
    var x = document.getElementById('admin');
    if('{{ role }}'=='admin'){

        if (x.style.display == 'none')
            x.style.display = 'block';
    }
    else
        x.style.display = 'none';
}

function func(id)
{
    var x = document.getElementById(id);
    if(x.style.display == "block")
        x.style.display = "none";
    else
        x.style.display = "block";
}

function LogOut()
{
    debugger;
    console.log('logging out');
    $.ajax({
        url:'/log_out',
        type:'post',
        data:{},
        success: function(resp)
        {
            if (resp['message']=='Success')
                window.location.href='/';
        }
    });
}

let slideIndex = 1;
showSlides(slideIndex);
function nextSlide() {
    showSlides(slideIndex += 1);
}

function previousSlide() {
    showSlides(slideIndex -= 1);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let slides = document.getElementsByClassName("item");

    if (n > slides.length) {
      slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }

    for (let slide of slides) {
        slide.style.display = "none";
    }

    slides[slideIndex - 1].style.display = "block";
}

