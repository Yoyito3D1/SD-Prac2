💾 Distributed Sharded Database System 💾
A hands-on project demonstrating the implementation of a distributed key-value storage system with sharding and fault-tolerant features! 🚀

🎯 Project Overview
This project builds a scalable distributed database where multiple nodes store data and a Shard Master manages the distribution. The system supports dynamic addition/removal of nodes, key redistribution, and automatic detection of server failures, showcasing practical concepts in distributed systems. ⚡

Implementation Highlights
- **Shard Master**: Controls key assignment and node ranges.
- **KVStorage Nodes**: Each node stores keys in a dictionary, supports transfer and redistribution.
- **Clients**: Interact via gRPC to query and store keys.
- **Scalability & Fault Tolerance**: Supports vertical and horizontal scaling, automatic redistribution, and leader election for replica masters.

🛠️ How It Works
1. **Client Requests**: Clients query or store data; requests go through the Shard Master to locate responsible nodes.
2. **Shard Master Management**: Tracks node ranges, updates assignments when nodes join/leave, and coordinates key redistribution.
3. **KVStorage Operations**: Nodes handle keys, synchronize via transfer/redistribute methods.
4. **Fault Tolerance**: Replica groups monitor each other (heartbeats); Paxos or Raft algorithms can elect a new replica master in case of failures.

🔍 System Features
- Dynamic shard allocation and key redistribution
- Support for adding/removing nodes on the fly
- Horizontal & vertical scalability
- Automatic failure detection and recovery
- Synchronization between nodes for consistent data storage

📚 Learning Goals
- Understand client-server communication in distributed systems
- Implement sharding strategies for load balancing
- Apply fault-tolerant mechanisms and leader election algorithms
- Gain hands-on experience with gRPC, replication, and key redistribution

📈 Real-World Inspiration
- **MongoDB**: Uses shard clusters, config servers, and Mongos routers for scalable NoSQL storage.
- **Apache Cassandra**: Uses ring-based nodes, replication, and consistency algorithms for distributed storage.

🙌 Contributions & Credits
Implemented as part of a Distributed Systems course practice. Thanks to open-source tools and concepts that guided this implementation: Python, gRPC, Paxos/Raft consensus.

📫 Contact & Support
For questions or discussions, feel free to open an issue or reach out! ✉️

Thank you for exploring this project! 🚀
Learn and experiment with distributed systems while building resilient and scalable architectures! 🌐💡
