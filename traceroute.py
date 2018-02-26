import subprocess

# Double paths?
# Cycles?

def parse_hops(traceroute_output):
	hops = []
	for row in traceroute_output:
		# Get rid of empty line
		if row == "":
			continue
		# Get rid of rows not containing two spaces
		arr = row.split("  ")
		if len(arr) == 1:
			continue
		# Get rid of * addresses
		if arr[1] == "*":
			continue
		# Don't append if duplicate address
		if arr[0] == arr[1]:
			continue

		#print "Hop:", arr[1]
		hops.append(arr[1])

	return hops


def get_pairs(ips):
	pairs = []
	for i in range(1, len(ips)):
		ip1 = ips[i]
		ip2 = ips[i-1]
		# Check for loops
		if ip1 == ip2:
			continue
		pairs.append([ip2, ip1])

	return pairs


# Add without inserting duplicates
def add_to(bulk, pairs):
	rtn = bulk
	for p in pairs:
		should_skip = 0
		for b in bulk:
			if p[0] == b[0] and p[1] == b[1]:
				print "Duplicate found:", p[0], p[1]
				should_skip = 1
		if not should_skip:
			rtn.append(p)
	return rtn


def save_output(pairs, ip=4):
	fo = open("router-topology-v"+str(ip)+".dot", "w")
	fo.write("graph routertopology {\n")

	for p in pairs:
		fo.write("\t\""+str(p[0])+"\" -- \""+str(p[1])+"\"\n")
	
	fo.write("}")
	fo.close


def main():
	f = open("lookup.txt", "r")

	ipv4_pairs = []
	ipv6_pairs = []

	while True:
		line = f.readline()[:-1]
		if (line == "" or line == "\n"):
			break

		array = line.split(" ")
		ip_addr = array[2]

		if (array[1] == "IPv6"):
			ip = 6
		else:
			ip = 4

		print "Tracing:", ip_addr
		p = subprocess.Popen(
			["traceroute", "-"+str(ip), "-q 1", "-n", ip_addr],
			stdout=subprocess.PIPE)
		output_array = p.communicate()[0].split("\n")

		hops = parse_hops(output_array)
		pairs = get_pairs(hops)
		print pairs
		
		if (ip == 6):
			ipv6_pairs = add_to(ipv6_pairs, pairs)
		else:
			ipv4_pairs = add_to(ipv4_pairs, pairs)

	save_output(ipv4_pairs)
	save_output(ipv6_pairs, ip=6)
	f.close()


if __name__ == '__main__':
	main()
