const showCategories = async (url) => {
    const response = await genericRequest(url, 'get')

    response.data.forEach(category => {
        $('#categorySelect').append(`<option value=${category['id']}>${category['name']}</option>`)
    })
}

function createPayload(id) {
    let formData = getFormData(id)
    const image = $('#headerPhoto')[0].files[0]
    if (image) {
        formData.append('header_photo', image)
    }
    return formData;
}

const createUpdatePost = async (id, postsListUrl, redirectUrl, method) => {
    const formData = createPayload(id);
    const headers = {'Content-Type': 'multipart/form-data'}
    const response = await genericRequest(postsListUrl, method,
        formData, headers)

    if (response.status === 200 || response.status === 201) {
        return window.location.href = redirectUrl.replace('1', response.data.id)
    }
}