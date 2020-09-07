document.addEventListener('DOMContentLoaded', function() {

	console.log("done")

	// Use buttons to toggle between views
	document.querySelector('#profileBtn').addEventListener('click', (event) => load_profile(event.currentTarget.value))
	document.querySelector('#postsBtn').addEventListener('click', () => load_posts("All Posts", new_page=true))
	document.querySelector('#followingBtn').addEventListener('click', () => load_posts("Posts by Following", new_page=true))

	// When form is submitted
	document.querySelector("#compose-form").addEventListener('submit', submit_form);

	// By default, load the inbox
	load_posts("All Posts", new_page=true)
});

function submit_form() {
	const post_text = document.querySelector("#text").value
	console.log(post_text)
	
	fetch('/create', {
		method: 'POST',
		body: JSON.stringify({
			"text": post_text
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print result
		console.log("updated")
		console.log(result)
	})
	
	document.querySelector("textarea").value = ""
	
	load_posts("All Posts", new_page=true)
}

function load_profile(user_id) {	
	
	// Update heading
	document.querySelector("h1").innerHTML = "Profile"
	
	// Show the mailbox and hide other views
	document.querySelector('#profile-view').style.display = 'block'
	document.querySelector('#form-view').style.display = 'none'
	document.querySelector('#posts-view').style.display = 'block'
	document.querySelector('#buttons-view').style.display = 'block'
	// To be changed
	
	fetch('/profile/'+user_id)
	.then(response => response.json())
	.then(response => {
		console.log(response)
		document.querySelector("#profile-view").innerHTML = display_profile(response)
		if (response.is_user === false) {
			document.querySelector("#follow").addEventListener("click", () => following(user_id))
		}
	})
	
	load_posts("User "+user_id, new_page=true)
}

function following(id) {
	follow_stats = document.querySelector("#follow-stats").innerHTML.split(" ")
	
	if (document.querySelector("#follow").innerHTML === "Follow") {
		to_follow = true
		message = JSON.stringify({
			"follow": 1
		})
		
		follow_stats[1] = parseInt(follow_stats[1]) + 1
		document.querySelector("#follow").innerHTML = "Unfollow"
		document.querySelector("#follow").className = "btn btn-danger"
	} else {
		to_follow = false
		message = JSON.stringify({
			"unfollow": 1
		})
		
		follow_stats[1] = parseInt(follow_stats[1]) - 1
		document.querySelector("#follow").innerHTML = "Follow"
		document.querySelector("#follow").className = "btn btn-success"
	}
	document.querySelector("#follow-stats").innerHTML = follow_stats.join(" ")
	
	fetch('/profile/'+id, {
		method: 'PUT',
		body: message
	})
}

function display_profile(profile) {
	let is_you = ""
	let follow_btn = ""
	if (profile.is_user === true) {
		is_you = "(You)"
	} else {
		if (profile.is_following === true) {
			follow_btn = `<button id="follow" type="button" class="btn btn-danger">Unfollow</button>`
		} else {
			follow_btn = `<button id="follow" type="button" class="btn btn-success">Follow</button>`
		}
	}
	divContent = `
	<div class="card">
		<div id="profile" class="card-body" align="center">
			<h3>${profile.user} ${is_you}</h3>
			<h5 id="follow-stats" class="text-secondary">Followers ${profile.num_of_followers} Following ${profile.num_of_following}</h5>
			${follow_btn}
		</div>
	</div>`
	
	return divContent
}

function load_posts(post_type, new_page=false) { // post_type is either "All Posts" or "Posts by Following" or "User (id)"

	console.log(post_type)
	
	// Get page number
	if (new_page === true) {
		var page_number = 1
	} else {
		var page_number = document.querySelector("#posts-view").querySelector("h4").innerHTML.slice(-1)
	}
	
	/*
	if (document.querySelector("#posts-view").querySelector("h4").innerHTML !== "") {
		// console.log(true)
		// console.log(post_type)
		// console.log(document.querySelector("h1").innerHTML)
		// console.log(document.querySelector("#posts-view").querySelector("h4").innerHTML.slice(-1))
		var page_number = document.querySelector("#posts-view").querySelector("h4").innerHTML.slice(-1)
		
		let h1 = ""
		if (post_type.includes("User")) {
			h1 = "Profile"
		} else {
			h1 = post_type
		}
		if (h1 !== document.querySelector("h1").innerHTML) {
			console.log(false)
			page_number = 1
		}
	} else {
		console.log(3)
		var page_number = 1
	}
	*/
	
	if (!post_type.includes("User")) { // If user is not on Profile page
		document.querySelector("h1").innerHTML = post_type // Update heading
		
		document.querySelector('#profile-view').style.display = 'none'
		document.querySelector('#form-view').style.display = 'block'
	} else {
		document.querySelector('#profile-view').style.display = 'block'
		document.querySelector('#form-view').style.display = 'none'
	}

	// Show the mailbox and hide other views
	// document.querySelector('#posts-view').style.display = 'block'
	// document.querySelector('#buttons-view').style.display = 'block'
	
	// Clear existing HTML
	document.querySelector('#posts-view').innerHTML = ""
	
	// Get emails, display them, and create 'click' event
	fetch('/posts/'+post_type+'/'+page_number)
	.then(response => response.json())
	.then(response => {
		
		const h4_element = document.createElement("h4")
		h4_element.setAttribute("class", "text-secondary")
		h4_element.innerHTML = "Page "+response.page_number
		document.querySelector("#posts-view").append(h4_element)
				
		response["posts"].forEach(function(post, index) {
			
			const element = document.createElement('div');
			element.setAttribute("class", "card")

			element.innerHTML = display_post(post, index)
			element.querySelector(".like").addEventListener("click", (event) => like(event.currentTarget.value, post.post_id))
			element.querySelector(".user").addEventListener("click", (event) => load_profile(event.currentTarget.value))
			
			if (post.is_user === true) {
				element.querySelector(".edit").addEventListener("click", (event) => edit(event.currentTarget.value, post.post_id))
			}
			
			document.querySelector('#posts-view').append(element)
		})
		
		document.querySelector("#buttons-view").innerHTML = display_page_toggle(response.has_next, response.has_previous)
		// Add events for both buttons
		document.querySelector("#nextPage").addEventListener("click", () => change_page(1, user_id=post_type.replace(/\D/g,'')))
		document.querySelector("#previousPage").addEventListener("click", () => change_page(-1, user_id=post_type.replace(/\D/g,'')))
	})
	
}

function edit(post_num, id) {
	
	post = document.querySelectorAll(".post")[post_num]
	newHTML = display_edit_post(post.querySelector(".post-body").innerHTML, post_num)
	post.innerHTML = newHTML
	
	post.querySelector("#edit-form").addEventListener("submit", () => {
		modify_form(id)
	})
	post.querySelector("#cancel-edit").addEventListener("click", () => reload_post(id=id))
}

function modify_form(id) {
	// Upload user changes to post body via API
	const post_text = document.querySelector("#edit-text").value
	
	// Make API call to like post
	fetch('/post/'+id, {
		method: 'PUT',
		body: JSON.stringify({
			"edit_body": post_text
		})
	})
	.then(response => response.json())
	.then(response => {
		console.log("updated")
		reload_post(id=0, post=response)
	})
}

function change_post_div(post) {
	const element = document.querySelector("#edit-form").parentElement
	index = Array.prototype.indexOf.call(document.querySelectorAll(".post"), element)
	element.innerHTML = "" // Delete existing form
	
	element.innerHTML = display_post(post, index)
	element.querySelector(".edit").addEventListener("click", (event) => edit(event.target.value, post.post_id))
	element.querySelector(".like").addEventListener("click", (event) => like(event.target.value, post.post_id))
}

function reload_post(id=0, post=false) {
	if (post === false) {
		fetch('/post/'+id)
		.then(response => response.json())
		.then(response => {
			change_post_div(response)
		})
	} else {
		change_post_div(post)
	}
}

function like(post_num, id) {
	
	post = document.querySelectorAll(".post")[post_num]
	if (post.querySelector(".like").innerHTML === "Like") {
		// Make API call to like post
		fetch('/post/'+id, {
			method: 'PUT',
			body: JSON.stringify({
				"like": true
			})
		})
		
		post.querySelector(".like").innerHTML = "Unlike"
		post.querySelector(".like").className = "btn btn-sm btn-outline-danger like"
		post.querySelector("#num_of_likes").innerHTML = parseInt(post.querySelector("#num_of_likes").innerHTML) + 1
	} else {
		// Make API call to unlike post
		fetch('/post/'+id, {
			method: 'PUT',
			body: JSON.stringify({
				"unlike": true
			})
		})
		
		post.querySelector(".like").innerHTML = "Like"
		post.querySelector(".like").className = "btn btn-sm btn-outline-success like"
		post.querySelector("#num_of_likes").innerHTML = parseInt(post.querySelector("#num_of_likes").innerHTML) -1
	}
	
}

function change_page(change, user_id=0) {
	// Get page number
	var page_number = parseInt(document.querySelector("h4").innerHTML.slice(-1)) + change
	
	// Update page number
	document.querySelector("#posts-view").querySelector("h4").innerHTML = "Page "+page_number
	
	if (document.querySelector("h1").innerHTML === "Profile") {
		load_posts("User "+user_id)
	} else {
		load_posts(document.querySelector("h1").innerHTML)
	}
}

function display_edit_post(body, index) {
	divContent = `
	<button id="cancel-edit" class="btn btn-outline-secondary float-right">Cancel</button>
	<form id="edit-form">
		<h5>Edit Post</h5>
		<div class="form-group">
			<textarea class="form-control" id="edit-text" rows="3">${body}</textarea><br>
			<button type="submit" class="btn btn-primary">Save</button>
		</div>
	</form>`
	
	return divContent
}

function display_post(post, index) {
	modify_button = ""
	if (post.is_user === true) {
		modify_button = `<button class="btn btn-outline-secondary float-right edit" value=${index}>Edit</button>`
	}
	
	like_button = `<button class="btn btn-sm btn-outline-success like" value=${index}>Like</button>`
	if (post.liked_by_user === true) {
		like_button = `<button class="btn btn-sm btn-outline-danger like" value=${index}>Unlike</button>`
	}
	
	divContent = `
	<div class="card-body post">
		${modify_button}
		<button class="btn btn-link user" value="${post.user_id}"><h5>${post.user}</h5></button>
		
		<p class="post-body">${post.body}</p>
		<p class="text-secondary">${post.timestamp}</p>
		${like_button}
		<p id="num_of_likes" style="display: inline">${post.likes}</p>
	</div>`

	return divContent
}

function display_page_toggle(has_next, has_previous) {
	next = "disabled"
	if (has_next === true) {next = ""}
	
	previous = "disabled"
	if (has_previous === true) {previous = ""}
	
	divContent = `
	<br>
	<div class="btn-group" role="group" aria-label="Basic example">
		<button id="previousPage" type="button" class="btn btn-secondary" ${previous}>Previous</button>
		<button id="nextPage" type="button" class="btn btn-secondary" ${next}>Next</button>
	</div>`
	
	return divContent
}