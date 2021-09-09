const showUsersPosts = async (url, redirectUrl, userId) => {
    $('#postDeck').empty()
    const response = await genericRequest(url, 'get')
    const usersPosts = response.data.filter(post => {
        return post['author']['id'] === userId
    })
    renderPostHtml(usersPosts, redirectUrl)
}