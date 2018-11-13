import struct
import uuid


def parse_mbr(mbr_bytes):
    List1=[]
    startval=0x1BE

    #list of dictionaries
    for x in range(4):
        Dictionaryparsed ={}

        partition=mbr_bytes[startval:]

        type1 = struct.unpack('<B',partition[4:5])[0]
        typereal=hex(type1)
        Dictionaryparsed["type"]=typereal
        start=struct.unpack("<I", partition[8:12])[0]
        Dictionaryparsed["start"]=start
        end=struct.unpack('<I', partition[12:16])[0]
        Dictionaryparsed["end"]=start + end-1
        Dictionaryparsed["number"]=x



        if type1!=0:
            List1.append(Dictionaryparsed)
            startval=startval + 16

    return List1




def parse_gpt(gpt_file, sector_size=512):
    #72-80 bytes starting lba
    #80-84 number of partition entries
    #84-88 Size of a single partition entry (usually 80h or 128)
    List1=[]
    gpt_file.seek(512)
    data=gpt_file.read(512)

    numberpart = struct.unpack("<I",data[80:84])[0]
    entrysize = struct.unpack("<I",data[84:88])[0]
    gpt_file.seek(struct.unpack("<Q",data[72:80])[0] * 512)
    part = gpt_file.read(numberpart * entrysize)

    for x in range(numberpart):
        Dictionaryparsed={}

        val = x * entrysize
        startparse=val+32

        if uuid.UUID(bytes_le=part[val:val+16]) != uuid.UUID(int=0):
            number = x
            Dictionaryparsed['number'] = number

            start = struct.unpack("<Q",part[startparse:startparse+8])[0]
            Dictionaryparsed['start']=start

            end = struct.unpack("<Q",part[startparse+8:startparse+16])[0]
            Dictionaryparsed['end']=end

            Dictionaryparsed['type']= uuid.UUID(bytes_le=part[val:val+16])
            nameparse=startparse+24

            Dictionaryparsed['name'] = part[nameparse:nameparse + 72].decode('utf-16-le').split('\x00')[0]

            List1.append(Dictionaryparsed)


    return List1










def main():
    pass


if __name__ == '__main__':
    main()