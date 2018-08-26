var $myForm = $('.post-form')
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
                        
                        $('ul').prepend("<li> <p class='content'>"+data['content']+"</p> <p>"+data['timestamp']+"</p> <p>Created by - "+data['created_by_name']+"</p> </li>")
                    }

                    function handleFormError(jqXHR, textStatus, errorThrown){
                        $("#loading-overlay").hide();
                        console.log(jqXHR)
                        console.log(textStatus)
                        console.log(errorThrown)
                    }
            });