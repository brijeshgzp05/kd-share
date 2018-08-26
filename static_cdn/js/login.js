$(document).ready(function(){
            var $myForm = $('.login-form')
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

                    

                    function handleFormError(jqXHR, textStatus, errorThrown){
                        $("#loading-overlay").hide();
                        $('#error_block').text('Wrong username or password')
                        console.log(jqXHR)
                        console.log(textStatus)
                        console.log(errorThrown)
                    }
            });
        });