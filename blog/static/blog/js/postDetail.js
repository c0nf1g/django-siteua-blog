const updateRecommendations = async (url) => {
    const response = await genericRequest(url, 'get')
    $('#recommendations').text(response.data['recommendations'].length)
}

const updateCommentSection = async (url, post_id) => {
    const getCommentsResponse = await genericRequest(url, 'get')
    const filteredComments = getCommentsResponse.data.filter((value) => {
        return value['post'] === post_id
    })
    showCommentsTest(filteredComments)
}

const showCommentsTest = (commentsCollection) => {
    $('#commentSection').empty()
    commentsCollection.forEach(comment => {
        const date = new Date(comment['published'])
        const timeAgo = getTimeAgo(date)

        $('#commentSection').prepend(`
            <div class="d-flex mb-4">
            <div class="flex-shrink-0"><img class="rounded-circle"
                                            src="${comment['author']['profile_photo']}"
                                            height="50"
                                            width="50">
                                            </div>
                <div class="ml-3">
                    <div>
                    <span class="font-weight-bold">${comment['author']['first_name']} ${comment['author']['last_name']}</span>
                     ${timeAgo}
                    </div>
                    <p>${comment['content']}</p>
                </div>
            </div>
        `)
    })
}

const addComment = async (post_id, commentsListUrl) => {
    let formData = getFormData('addCommentForm')
    formData.append('post', post_id)
    await genericRequest(commentsListUrl, 'post', formData)
    await updateCommentSection(commentsListUrl, post_id)
}

const addRecommendation = async (recommendation,
                                 user_email,
                                 postDetailUrl,
                                 postRecommendUrl) => {
    const getPostResponse = await genericRequest(postDetailUrl, 'get')
    recommendation = !getPostResponse.data['recommendations'].includes(user_email);
    const payload = {'recommendation': recommendation}
    await genericRequest(postRecommendUrl, 'put', payload)
    await updateRecommendations(postDetailUrl)
}

