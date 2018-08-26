$(document).ready(function(){

        var $myForm = $('.code-form')
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
                    $('.form-div').fadeOut(500);
                    $('.login-div').delay(500).fadeIn(500);
                }

                function handleFormError(jqXHR, textStatus, errorThrown){
                	$("#loading-overlay").hide();
                        var obj = jQuery.parseJSON( jqXHR.responseText );
                        var div = $('.error_block center');
                        div.empty();

                        if (obj.code){
                            div.append("<p>"+obj.code+"</p>")
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