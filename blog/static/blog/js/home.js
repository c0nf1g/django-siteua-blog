const showPosts = async (url, redirectUrl) => {
    $('#postDeck').empty()
    const response = await genericRequest(url, 'get')
    response.data = filterPostsByCategory($('#selectCategory').val(), response.data)
    sortPostsByParameter($('#selectSortParameter').val(), response.data)
    renderPostHtml(response.data, redirectUrl)
}

const renderPostHtml = (postCollection, redirectUrl) => {
    postCollection.forEach(post => {
        if (post['header_photo'] === null) {
            post['header_photo'] = '/media/posts_images/default-post-img.png'
        }

        $('#postDeck').append(`
            <div class="col-md-6 pb-4">
                <div class="card">
                    <a href="${redirectUrl.replace('1', post.id)}" class="stretched-link"></a>
                    <img class="image-cap card-img-top" src="${post['header_photo']}" alt="Card image cap">
                    <div class="card-body">
                        <h5 class="card-title">${post['title']}</h5>
                        <p class="card-text"><small class="text-muted">${getTimeAgo(post['published'])}</small></p>
                    </div>
                </div>
            </div>
        `)
    })
}

const filterPostsByCategory = (selectedCategory, postCollection) => {
    if (selectedCategory === 'all') {
        return postCollection
    }

    return postCollection.filter((post) => {
        return post['category'] === selectedCategory
    })
}

const sortPostsByParameter = (sortParameter, postCollection) => {
    switch (sortParameter) {
        case 'newer':
            postCollection.sort((a, b) => {
                return new Date(b['published']) - new Date(a['published'])
            })
            break
        case 'older':
            postCollection.sort((a, b) => {
                return new Date(a['published']) - new Date(b['published'])
            })
            break
        case 'recommendations':
            postCollection.sort((a, b) => {
                return b['recommendations'].length - a['recommendations'].length
            })
            break
        case 'views':
            postCollection.sort((a, b) => {
                return b['views'] - a['views']
            })
            break
    }
}

const showFilterCategories = async (categoriesListUrl) => {
    const response = await genericRequest(categoriesListUrl, 'get')

    response.data.forEach(category => {
        $('#selectCategory').append(`<option value=${category['name']}>${category['name']}</option>`)
    })
}