const dotenv = require('dotenv');
dotenv.config();
const bodyParser = require('body-parser')
const express = require('express');
const app = express();
const port = 3000;
const parser = require('./parser');
const db = require('./db');

db.init(() => console.log('DB connected!'));
app.use(bodyParser.json())

app.post('/posts', async (req, res) => {
    try {
        const data = req.body;
        const pen = await db.Pen.create(data);

        res.status(200).send({
            success: true,
            data: pen,
        });
    } catch (e) {
        console.log(e);
        res.status(500).send({
            success: false,
            error: e,
        });
    }
})

app.get('/posts/:id', async (req, res) => {
    const postId = req.params.id;
    if (!postId) {
        res.status(500).send({success: false, error: 'Post id is required'});
        return;
    }

    try {
        const post = await db.Pen.findOne({ where: { id: postId } });
        if (!post) res.status(500).send({success: false, error: 'Wrong id'});

        res.status(200).send({success: true, data: post});
    } catch (e) {
        console.log(e);
        res.status(500).send({success: false, error: e});
    }
})

app.get('/posts', async (req, res) => {
    const { offset = '0', limit = '5' } = req.query;
    try {
        const { rows } = await db.Pen.findAndCountAll({
            where: { posted: false },
            offset: parseInt(offset),
            limit: parseInt(limit),
        });

        res.status(200).send({success: true, data: rows});
    } catch (e) {
        console.log(e);
        res.status(500).send({success: false, error: e});
    }
})

app.get('/posts/mark/:id', async (req, res) => {
    const data = req.params;
    console.log(data.id)
    if (!data.id) {
        res.status(500).send({success: false, error: 'Id is required!'});
    }
    try {
        const pen = await db.Pen.findOne({ where: { id: data.id } });
        if (pen) {
            await pen.update({ posted: true });
            res.status(200).send({success: true, data: pen});
        } else {
            res.status(500).send({success: false, error: 'Pen not found'});
        }
    } catch (e) {
        console.log(e);
        res.status(500).send({success: false, error: e});
    }
})

app.get('/parse', async (req, res) => {
    try {
        const posts = await parser.getPosts();

        if (!posts.length) {
            console.log('There is no posts');
        }

        res.status(200).send({success: true, data: posts});
    } catch (e) {
        console.log(e);
        res.status(500).send({success: false, error: e});
    }
})

app.listen(port, () => {
    console.log(`Parser app listening on port ${port}`);
})
