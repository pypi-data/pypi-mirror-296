import socket as S
import struct

def build_dns_qry(domain):
    # Header fields
    ID = 11451      # Identification
    FLAGS = 0x0100   # Standard query with recursion
    QDCOUNT = 1      # Number of questions
    ANCOUNT = 0      # Number of answers
    NSCOUNT = 0      # Number of authority records
    ARCOUNT = 0      # Number of additional records

    header = struct.pack('>HHHHHH', ID, FLAGS, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT)

    # Query section
    query = b''
    for part in domain.split('.'):
        query += struct.pack('B', len(part)) + part.encode('utf-8')
    query += struct.pack('B', 0)  # End of the domain part
    
    QTYPE = 1  # Type A (host address)
    QCLASS = 1 # Class IN (internet)
    
    query += struct.pack('>HH', QTYPE, QCLASS)
    return header + query


def parse_dns_rsp(rsp):
    # Header part (12 bytes)
    transaction_id = rsp[:2]
    flags = rsp[2:4]
    questions = rsp[4:6]
    answer_rrs = rsp[6:8]
    authority_rrs = rsp[8:10]
    additional_rrs = rsp[10:12]
    
    tid = struct.unpack('>H', transaction_id)[0]
    flags = struct.unpack('>H', flags)[0]
    questions = struct.unpack('>H', questions)[0]
    answer_rrs = struct.unpack('>H', answer_rrs)[0]
    authority_rrs = struct.unpack('>H', authority_rrs)[0]
    additional_rrs = struct.unpack('>H', additional_rrs)[0]

    # Skip all other parts
    return {
        "tid": tid,
        "flags": flags,
        "questions": questions,
        "answer_rrs": answer_rrs,
        "authority_rrs": authority_rrs,
        "additional_rrs": additional_rrs
    }
