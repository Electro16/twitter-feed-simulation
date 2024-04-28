// frontend\src\App.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const ENDPOINT = 'http://localhost:5000'; // Replace with your Flask server endpoint

const App = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const socket = io(ENDPOINT);

    socket.on('new_post', (newPost) => {
      setPosts((prevPosts) => [...prevPosts, newPost]);
    });

    return () => socket.disconnect();
  }, []);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch(`${ENDPOINT}/posts`);
        const data = await response.json();
        setPosts(data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    fetchPosts();
  }, []);

  return (
    <div>
      <h1>Post List</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <strong>{post.title}</strong>
            <p>{post.body}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
