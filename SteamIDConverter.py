import urllib2, re
from xml.dom import minidom

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  see http://dl.dropbox.com/u/1502097/SteamIDtoCommunityID.pdf
  for more information regarding these conversions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

userURL = "http://steamcommunity.com/id/{USER}/?xml=1"
idURL = "http://steamcommunity.com/profiles/{ID}/?xml=1"
steamIDBase = 76561197960265728

def convertCommunityIDToCustomURL(communityID):
	dom = minidom.parse(urllib2.urlopen(re.sub("{ID}", str(communityID), idURL)))
	customURL = dom.getElementsByTagName("customURL")[0].firstChild.data
	return customURL

def convertCommunityIDToSteamID(communityID):
	steamID = []
	steamID.append("STEAM_0:")
	steamIDLastPart = communityID - steamIDBase
	if steamIDLastPart % 2 == 0:
		steamID.append("0:")
	else:
		steamID.append("1:")
	steamID.append(str(steamIDLastPart // 2))
	return "".join(steamID)

def convertCustomURLToCommunityID(customURL):
	dom = minidom.parse(urllib2.urlopen(re.sub("{USER}", customURL, userURL)))
	communityID = dom.getElementsByTagName("steamID64")[0].firstChild.data
	return int(communityID)

def convertCustomURLToSteamID(customURL):
	communityID = convertCustomURLToCommunityID(customURL)
	return convertCommunityIDToSteamID(communityID)

def convertSteamIDToCommunityID(steamID):
	steamIDParts = re.split(":", steamID)
	communityID = int(steamIDParts[2]) * 2
	if steamIDParts[1] == "1":
		communityID += 1
	communityID += steamIDBase
	return communityID

def convertSteamIDToCustomURL(steamID):
	communityID = convertSteamIDToCommunityID(steamID)
	return convertCommunityIDToCustomURL(communityID)

if __name__ == "__main__":
	userInput = raw_input("Enter a custom url, community id, or steam id: ")
	if userInput.startswith("STEAM_0:"):
		steamID = userInput
		communityID = convertSteamIDToCommunityID(steamID)
		customURL = convertCommunityIDToCustomURL(communityID)
	elif re.match("^\d*$", userInput):
		communityID = int(userInput)
		steamID = convertCommunityIDToSteamID(communityID)
		customURL = convertCommunityIDToCustomURL(communityID)
	else:
		# assuming valid custom url
		customURL = userInput
		communityID = convertCustomURLToCommunityID(customURL)
		steamID = convertCommunityIDToSteamID(communityID)
	print "Custom URL:", customURL
	print "Community ID:", communityID
	print "Steam ID:", steamID