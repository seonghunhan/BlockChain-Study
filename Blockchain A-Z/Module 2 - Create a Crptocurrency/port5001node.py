#Module 2 - Create a Cryptocurrency

# Flask == 0.12.2
# request == 2.18.4

import datetime
import hashlib
import json
# jsonify 이용해서 json형식으로 채굴된 새로운 블록의 핵심 정보로 돌아간다
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


# Part1 - Building a Blockchain

class Blockchain :
      
      def __init__(self):
            # 나중에 채굴할 다른 블록에 첨부할 것
            self.chain = []
            
            # 제네시스 블록 전에 트랜잭션 모아야함 (암호화폐)
            self.transactions = []
            
            # 제네시스블록은 preHash없지
            self.create_block(proof = 1, previous_hash = '0')
            
            #(암호화폐)
            self.nodes = set()
        
      #채굴 직후에 사용될예정 그래서 작업 증명 문제에 기반한 증명제공
      def create_block(self, proof, previous_hash) :
            
            #채굴된 새블록 정의 -> prrof는 nonce로 쓰이는듯?
            block = {'index' : len(self.chain) + 1,
                     'timestamp' : str(datetime.datetime.now()),
                     'proof' : proof,
                     'previous_hash' : previous_hash,
                     'transactions' : self.transactions}
            
            # 트랜잭션 비우기(암호화폐)
            self.transactions = []
            
            self.chain.append(block)
            
            return block
      
      def get_previous_block(self) :
            #체인 리스트에있는 마지막블록 반환
            return self.chain[-1]
      
      #작업증명 : 채굴자들이 새로운 블록을 채굴하기 위해 찾아내야하는 데이터 또는 숫자
      def proof_of_work(self, previous_proof) :
            # 1부터 시작하여 시행착오 겪을것
            new_proof = 1
            check_proof = False
            
            while check_proof is False :
                  #연산이 대칭이기 때문
                  #여기가 좀 이해안감 이과정으로 어캐 찾는다는거지
                  #채굴자들이 풀어야하는 식을 임의로 만든듯?
                  hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
                  
                  #선행제로가 존재하면 확인 증명 성공
                  if hash_operation[:4] == '0000' :
                        check_proof = True
                  else :
                        new_proof += 1
                        
            return new_proof
      
      #블록의 정보를 가지고 해쉬암호 반환
      def hash(self, block) :
            #dumps함수로 블록 딕셔너리를 문자열로 바꾸기
            encoded_block = json.dumps(block, sort_keys = True).encode()
            
            return hashlib.sha256(encoded_block).hexdigest()

      # 블록체인의 유효성 확인 1.이전 해시와 동일한지 2. 작업 증명 문제에 따라 유효한지
      def is_chain_valid(self, chain) :
            previous_block = chain[0]
            block_index = 1
            
            while block_index < len(chain) :
                  block = chain[block_index]
                  
                  # 모든 블록은 이전블록의 해쉬와 같아야함 한개라도 틀리면 False반환
                  if block['previous_hash'] != self.hash(previous_block) :
                        return False

                  previous_proof = previous_block['proof']
                  proof = block['proof']
                  hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
                  
                  #작업 증명의 선행 제로가 4개가 아닐경우 False반환
                  if hash_operation[:4] != '0000' :
                        return False
                  
                  #현재블록을 이전블록으로
                  previous_block = block
                  #다음블록 탐색하기 위함
                  block_index += 1
            
            return True
          
          
        #채굴자가 새로운 블록을 채굴하면 거기로 가기
        # 트랜잭션 모으기(암호화폐)
      def add_transaction(self, sender, receiver, amount) :
            self.transactions.append({'sender' : sender,
                                        'receiver' : receiver,
                                        'amount' : amount})
            
            previous_block = self.get_previous_block()
            
            #이 트랜잭션은 새로생길(마지막인덱스의 +1)로 갈것임
            return previous_block['index'] + 1   
        
        #네트워크에 노드 추가, 여기서 address는 url
      def add_node(self, address) :
          #parsed_url 이거 프린트해보면 http, 127.0.01~:포트번호 이런거 나옴
          parsed_url = urlparse(address)
          #위에서 파싱한 url의 정보중 127.0.0~:포트번호 이런것만 추가하겠다는거임
          self.nodes.add(parsed_url.netloc)
          
      def replace_chain(self):
          #전세계 노드의 전부를 network로 정의
          network = self.nodes
          longest_chain = None
          max_length = len(self.chain)
          
          #네트워크상 모든 노드 반복
          for nodes in network :
              #API활용 -> requests의 get메소드 활용
              #포트는 노드의 포트를 따르기에 바뀜, 아래 이거 http://192.168.0.13:5000/get_chain이거랑 같음 신기하노
              response = requests.get(f'http://{nodes}/get_chain')
              if response.status_code == 200 :
                  length = response.json()['length']
                  chain = response.json()['chain']
                  
                  #길이가 맥스보다 큰지와 유효한지 검사
                  if length > max_length and self.is_chain_valid(chain) :
                      max_length = length
                      longest_chain = chain
          
          # 체인 업댓됐다는것 의미
          if longest_chain :
              self.chain = longest_chain
              return True
          
          return False            
              
           
# Part2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-','')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block() :
      #증명을 얻기위해선 작업 증명을 해야함
      previous_block = blockchain.get_previous_block()
      previous_proof = previous_block['proof']
      proof = blockchain.proof_of_work(previous_proof)
      previous_hash = blockchain.hash(previous_block)
      blockchain.add_transaction(sender = node_address, receiver = '5001A', amount = 1) #암호화폐
      block = blockchain.create_block(proof, previous_hash)
      
      response = {'message' : '축하해, 너는 블록을 채굴했어!',
                  'index' : block['index'],
                  'timestamp ' : block['timestamp'],
                  'proof' : block['proof'],
                  'previous_hash' : block['previous_hash'],
                  'transactions' : block['transactions']}
      
      return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain() :
      # 초기에는 빈리스트지만 mine블럭하면 풀체인으로 바뀌어있을것임
      response = {'chain' : blockchain.chain, 
                  'length' : len(blockchain.chain)}
      
      return jsonify(response), 200

# Checking if the Blockvhain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
      is_valid = blockchain.is_chain_valid(blockchain.chain)
      
      if is_valid :
            response = {'Message' : 'All good'}
      else :
            response = {'Message' : 'we have a problem, the blockchain is not valid'}
            
      return jsonify(response)

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction() :
    #POST메서드로 리퀘스트 파싱하는방법
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys) :
        return '트랜잭션에서 몇몇 요소가 누락되었다!', 400
    
    # json은 딕셔너리랑 같게 동자하니까 저렇게 파싱 가능
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message' : f'이 트랜잭션은 추가될거야 {index}'}
    return jsonify(response), 201 # 201은 성공적으로 writing되었다는 뜻 같음



# Part 3 - Decentalizing our Blockchain

# Connecting new nodes
# 탈중앙화에 새로운 노드 등록 -> POST
@app.route('/connect_node', methods=['POST'])
def conect_node() :
      json = request.get_json()
      #리퀘할때 키값중 nodes선택    
      nodes = json.get('nodes')
      if nodes is None :
            return "No node" , 400
      
      for node in nodes :
            blockchain.add_node(node)
      response = {'message' :'All the nodes are now connected. The 훈 Blockchain now contains the ' ,
                  'total_nodes' : list(blockchain.nodes)}
      
      return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
      #체인이 가장 길어서 교체가 필요없는경우 False 반환
      is_chain_replaced = blockchain.replace_chain()
      
      if is_chain_replaced :
            response = {'Message' : 'The nodes had different chains so the chain was replaced by the longest chain',
                        'new_chain' : blockchain.chain} #블록체인 클래스의 채인 인스턴스를 호출
      else :
            response = {'Message' : 'All good. The chain is the largest one',
                        'actual_chain' : blockchain.chain}
            
      return jsonify(response), 200


# Running the app
app.run(host='0.0.0.0', port = 5001)