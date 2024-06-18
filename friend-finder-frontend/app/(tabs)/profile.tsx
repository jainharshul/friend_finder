import React, { useEffect, useState } from 'react';
import { StyleSheet, Image, Text, View, FlatList } from 'react-native';
import axios from 'axios';

const posts = [
  { id: '1', imageUri: 'https://example.com/post1.jpg', caption: 'Enjoying the sunshine!' },
  { id: '2', imageUri: 'https://example.com/post2.jpg', caption: 'Loving this new recipe!' },
  // Add more posts here
];

export default function TabThreeScreen() {
  const [profilePicture, setProfilePicture] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfilePicture = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:8000/token', {
          username: 'string',
          password: 'string',
        });
        const accessToken = response.data.access_token;
        const profileResponse = await axios.get('http://127.0.0.1:8000/profile/picture', {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        setProfilePicture(`data:image/png;base64,${profileResponse.data.profile_picture}`);
      } catch (error) {
        console.error('Failed to fetch profile picture', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfilePicture();
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Image source={profilePicture ? { uri: profilePicture } : require('../../assets/images/profile.png')} style={styles.profileImage} />
        <Text style={styles.name}>Harshul Jain</Text>
        <Text style={styles.username}>@hersheysbar</Text>
        <Text style={styles.bio}>Taco Bell</Text>
        <View style={styles.statsContainer}>
          <View style={styles.stat}>
            <Text style={styles.statNumber}>120</Text>
            <Text style={styles.statLabel}>Posts</Text>
          </View>
          <View style={styles.stat}>
            <Text style={styles.statNumber}>500</Text>
            <Text style={styles.statLabel}>Followers</Text>
          </View>
          <View style={styles.stat}>
            <Text style={styles.statNumber}>300</Text>
            <Text style={styles.statLabel}>Following</Text>
          </View>
        </View>
      </View>
      <FlatList
        data={posts}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <View style={styles.post}>
            <Image source={{ uri: item.imageUri }} style={styles.postImage} />
            <Text style={styles.caption}>{item.caption}</Text>
          </View>
        )}
        style={styles.postsList}
        contentContainerStyle={{ alignItems: 'center' }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f8f8f8',
    borderBottomWidth: 1,
    borderBottomColor: '#e1e1e1',
  },
  profileImage: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: 10,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  username: {
    fontSize: 16,
    color: '#666',
    marginBottom: 10,
  },
  bio: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
    marginBottom: 20,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
  },
  stat: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  statLabel: {
    fontSize: 14,
    color: '#666',
  },
  postsList: {
    flex: 1,
  },
  post: {
    marginVertical: 10,
    width: '90%',
    alignItems: 'center',
  },
  postImage: {
    width: '100%',
    height: 200,
    borderRadius: 10,
  },
  caption: {
    marginTop: 10,
    fontSize: 14,
    color: '#333',
  },
});
