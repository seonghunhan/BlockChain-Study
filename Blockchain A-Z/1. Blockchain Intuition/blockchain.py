#Module 1 - Crate a Blockchain

# Flask == 0.12.2

import datetime
import hashlib
import json
# jsonify 이용해서 json형식으로 채굴된 새로운 블록의 핵심 정보로 돌아간다
from flask import Flask, jsonify

# Creating a Wep App



# Part1 - Building a Blockchain

class Blockchain :
      
      def __init__(self):
            # 나중에 채굴할 다른 블록에 첨부할 것
            self.chain = []
            
            # 제네시스블록은 preHash없지
            self.create_block(proof = 1, previous_hash = '0')
        
      #채굴 직후에 사용될예정 그래서 작업 증명 문제에 기반한 증명제공
      def create_block(self, proof, previous_hash) :
            
            #채굴된 새블록 정의 -> prrof는 nonce로 쓰이는듯?
            block = {'index' : len(self.chain) + 1,
                     'timestamp' : str(datetime.datetime.now()),
                     'proof' : proof,
                     'previous_hash' : previous_hash}
            
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
                  
                  if hash_operation[:4] != '0000' :
                        return False
                  
                  previous_block = block
                  block_index += 1
            
            return True
                  
# Part2 - Mining our Blockchain
