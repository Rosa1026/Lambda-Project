$(document).ready(function(){
    var ENDPOINT = 'https://02x7yv1yv5.execute-api.ap-northeast-3.amazonaws.com/dev/reserve'
    var CF = 'https://d2ltyemy31vr0.cloudfront.net'
    var dialog = document.querySelector('dialog');
    var showModalButton = $('.show-modal');
    if (! dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    $("#start_date").on('change',function(){
        $('#end_date').attr("min",$("#start_date").val());
    })
    $("#end_date").on('change',function(){
        $('#start_date').attr("max",$("#end_date").val());
    })
    $(document).on('click', '.show-modal', function(e) {
        e.preventDefault();
        var user = $(this).data('user');
        var type = $(this).data('type');
        $('#showBox').html('<img style="width:100%" src="'+CF+'/qrcodes/'+user+'/'+type+'/qrcode.jpg"/>');
        dialog.showModal();
    });
    dialog.querySelector('.close').addEventListener('click', function() {
        dialog.close();
    });
    dialog.querySelector('.print').addEventListener('click', function() {
        print();
    });
    function load_data(){
        $.ajax({
            url: ENDPOINT +'/users/*',
            method: 'get',
            success: function(r){
                var html = '';
                html += '<ul class="demo-list-three mdl-list mdl-cell mdl-cell--4-col">'
                r['items'].forEach(function(item) {
                    html += '<li class="mdl-list__item mdl-list__item--three-line"> <span class="mdl-list__item-primary-content"> <i class="material-icons mdl-list__item-avatar">person</i> <span>'
                    html += item['user_name']
                    html += '</span> <span class="mdl-list__item-text-body">'
                    html += item['start_date'] +'~'+item['end_date']+'<br/> '+item['type']
                    html += '</span> </span> <span class="mdl-list__item-secondary-content"> <a data-user="'+item['user_id']+'" data-type="'+item['type']+'" class="show-modal mdl-list__item-secondary-action" href="#"><i class="material-icons">print</i></a> </span> </li>'
                })
                html += '</ul>'
                $('#history').html(html);
            },
            fail: function(err){
                console.log('failed', err);
            },
            complete: function(r){
                console.log('completed', r);
            }
        });
    }
    $('#submitButton').on('click', function(e){
        var user_id = $('#user_id').val();
        var type = $('#type').val();
        var user_name = $('#user_name').val();
        var user_phone = $('#phone_number').val();
        var start_date = $('#start_date').val();
        var end_date = $('#end_date').val();
        $.ajax({
            url: ENDPOINT,
            method: 'post',
            datatype: 'json',
            async: true,
            data:JSON.stringify({
                type: type,
                user_id: user_id,
                user_name: user_name,
                phone_number: user_phone,
                start_date: start_date,
                end_date :end_date
            }),
            beforeSend: function(){
                $('#p2').show();
            },
            success: function(r){
                console.log('success', r);
            },
            fail: function(err){
                console.log('failed', err);
                alert('failed! reloading...')
            },
            complete: function(r){
                console.log('completed', r);
                setTimeout(function() {
                    $('#p2').hide();
                    location.reload();
                }, 1000);
            }
        });
    });
    load_data();
})