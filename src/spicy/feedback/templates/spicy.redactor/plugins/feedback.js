{% load sk %}{% load url from future %}function(buttonName, buttonDom, buttonObj) {
    var obj = this
    var imglist = {% captureas field_id %}id_{{ field.html_name }}{% endcaptureas %}'{% url "feedback:admin:provider-form" consumer_type form.instance.pk field_id %}'
    $.get(imglist, function(data){
        obj.modalInit('{{ plugin.title }}', data, 500)
    })
}
