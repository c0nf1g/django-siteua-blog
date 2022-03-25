axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;

const genericRequest = async (url, method, payload={}, headers={}) => {
    return await axios({
        headers: headers,
        url: url,
        method: method,
        data: payload
    })
}

const getFormData = (id) => {
    const formData = new FormData()
    $(`#${id}`).serializeArray().forEach(element => {
        formData.append(element.name, element.value)
    })
    return formData
}

