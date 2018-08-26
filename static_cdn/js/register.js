$(document).ready(function(){
            

            var $myForm = $('.reg-form')
            $myForm.submit(function(event){
                event.preventDefault()
                var $formData = $(this).serialize()
                var $endPoint = $myForm.attr('data-url') || window.location.href // or set your own url
                $.ajax({
                    method: "POST",
                    url: $endPoint,
                    data: $formData,
                    beforeSend: function(){
                        $("#loading-overlay").show();
                    },
                    success: handleFormSuccess,
                    error: handleFormError,
                });

                    function handleFormSuccess(data, textStatus, jqXHR){
                        $("#loading-overlay").hide();
                        console.log(data)
                        console.log(textStatus)
                        console.log(jqXHR)
                        $myForm[0].reset(); 

                        $('.form-div').fadeOut(200);
                        $('.login-btn-div').delay(200).fadeIn(100);
                    }

                    function handleFormError(jqXHR, textStatus, errorThrown){
                        $("#loading-overlay").hide();
                        var obj = jQuery.parseJSON( jqXHR.responseText );
                        var div = $('.error_block center');
                        div.empty();

                        if (obj.email){
                            div.append("<p>"+obj.email+"</p>")
                        }
                        if (obj.mobile){
                            div.append("<p>"+obj.mobile+"</p>")
                        }
                        if (obj.username){
                           div.append("<p>"+obj.username+"</p>")
                        }
                        if (obj.password){
                            div.append("<p>"+obj.password+"</p>")
                        }
                        if (obj.cpassword){
                            div.append("<p>"+obj.cpassword+"</p>")
                        }

                        console.log(jqXHR)
                        console.log(textStatus)
                        console.log(errorThrown)
                    }
            });
         
        });