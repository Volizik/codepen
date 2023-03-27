const dotenv = require('dotenv');
const express = require('express');
const app = express()
const port = 3000
const parser = require('./parser')

dotenv.config();

let tmpPosts = [];

app.get('/posts', async (req, res) => {
    const postId = req.query.id;
    try {
        if (postId) {
            console.log({postId})
            // get from db
            const post = tmpPosts.find(({ link }) => link === postId);
            if (!post) res.status(500).send('Wrong id');
            // check if post already exist in db
            // save to db
            res.status(200).send(post);
        } else {
            const posts = await parser.getPosts();

            if (!posts.length) {
                console.log('There is no posts')
            }
            // save to db
            tmpPosts = posts;

            res.status(200).send(posts);
        }
    } catch (e) {
        console.log(e);
        res.status(500).send(e);
    }
})

app.listen(port, () => {
    console.log(`Parser app listening on port ${port}`);
})
