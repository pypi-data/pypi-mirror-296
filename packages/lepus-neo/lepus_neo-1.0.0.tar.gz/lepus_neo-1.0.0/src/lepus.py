#!/usr/bin/env python3

from argparse import ArgumentParser, FileType
from warnings import simplefilter
from termcolor import colored
from time import sleep
from gc import collect
import os
import subprocess
import globals
import collectors.Censys
import collectors.CertSpotter
import collectors.CRT
import collectors.DNSTrails
import collectors.FOFA
import collectors.GoogleTransparency
import collectors.HackerTarget
import collectors.PassiveTotal
import collectors.PDChaos
import collectors.ProjectCrobat
import collectors.ProjectSonar
import collectors.Riddler
import collectors.Shodan
import collectors.Spyse
import collectors.ThreatCrowd
import collectors.ThreatMiner
import collectors.VirusTotal
import collectors.WaybackMachine
import collectors.ZoomEye
import submodules.Permutations
import submodules.PortScan
import submodules.ReverseLookups
import submodules.TakeOver
import submodules.Markov
import utilities.DatabaseHelpers
import utilities.MiscHelpers
import utilities.ScanHelpers

simplefilter("ignore")
version = "3.4.0"
LEPUS_BLANK_INI = "[Censys]\nCENSYS_UID=\nCENSYS_SECRET=\n\n[DNSTrails]\nDNSTRAILS_API_KEY=\n\n[FOFA]\nFOFA_EMAIL=\nFOFA_KEY=\n\n[PassiveTotal]\nPT_KEY=\nPT_SECRET=\n\n[PDChaos]\nCHAOS_API_KEY=\n\n[Riddler]\nRIDDLER_USERNAME=\nRIDDLER_PASSWORD=\n\n[Shodan]\nSHODAN_API_KEY=\n\n[Slack]\nSLACK_LEGACY_TOKEN=\nSLACK_CHANNEL=\n\n[Spyse]\nSPYSE_API_TOKEN=\n\n[VirusTotal]\nVT_API_KEY=\n\n[ZoomEye]\nZOOMEYE_API_KEY=\n"


def printBanner():
    print(colored("         ______  _____           ______", "yellow"))
    print(colored(" |      |______ |_____) |     | (_____ ", "yellow"))
    print(colored(" |_____ |______ |       |_____| ______)", "yellow"))
    print(colored("                                v{0}".format(version), "cyan"))
    sleep(1)
def main():
    parser = ArgumentParser(prog="lepus.py", description="Infrastructure OSINT")
    parser.add_argument("domain", help="domain to search")
    parser.add_argument("-w", "--wordlist", action="store", dest="wordlist", help="wordlist with subdomains", type=FileType("r"))
    parser.add_argument("-hw", "--hide-wildcards", action="store_true", dest="hideWildcards", help="hide wildcard resolutions", default=False)
    parser.add_argument("-t", "--threads", action="store", dest="threads", help="number of threads [default is 100]", type=int, default=100)
    parser.add_argument("-nc", "--no-collectors", action="store_true", dest="noCollectors", help="skip passive subdomain enumeration", default=False)
    parser.add_argument("-zt", "--zone-transfer", action="store_true", dest="zoneTransfer", help="attempt to zone transfer from identified name servers", default=False)
    parser.add_argument("--permutate", action="store_true", dest="permutate", help="perform permutations on resolved domains", default=False)
    parser.add_argument("-pw", "--permutation-wordlist", dest="permutation_wordlist", help="wordlist to perform permutations with, seperated by comma [default is seclists, assumes installed]", type=str, default="/usr/share/seclists/Discovery/DNS/deepmagic.com-prefixes-top500.txt,/usr/share/seclists/Fuzzing/environment-identifiers.txt")
    parser.add_argument("--reverse", action="store_true", dest="reverse", help="perform reverse dns lookups on resolved public IP addresses", default=False)
    parser.add_argument("-ripe", "--ripe", action="store_true", dest="ripe", help="query ripe database with the 2nd level domain for networks to be used for reverse lookups", default=False)
    parser.add_argument("-r", "--ranges", action="store", dest="ranges", help="comma seperated ip ranges to perform reverse dns lookups on", type=str, default=None)
    parser.add_argument("-or", "--only-ranges", action="store_true", dest="only_ranges", help="use only ranges provided with -r or -ripe and not all previously identified IPs", default=False)
    parser.add_argument("--portscan", action="store_true", dest="portscan", help="scan resolved public IP addresses for open ports", default=False)
    parser.add_argument("-p", "--ports", action="store", dest="ports", help="set of ports to be used by the portscan module [default is medium]", type=str)
    parser.add_argument("--takeover", action="store_true", dest="takeover", help="check identified hosts for potential subdomain take-overs", default=False)
    parser.add_argument("--markovify", action="store_true", dest="markovify", help="use markov chains to identify more subdomains", default=False)
    parser.add_argument("-ms", "--markov-state", action="store", dest="markov_state", help="markov state size [default is 3]", type=int, default=3)
    parser.add_argument("-ml", "--markov-length", action="store", dest="markov_length", help="max length of markov substitutions [default is 5]", type=int, default=5)
    parser.add_argument("-mq", "--markov-quantity", action="store", dest="markov_quantity", help="max quantity of markov results per candidate length [default is 5]", type=int, default=5)
    parser.add_argument("-f", "--flush", action="store_true", dest="doFlush", help="purge all records of the specified domain from the database", default=False)
    parser.add_argument("-v", "--version", action="version", version="Lepus v{0}".format(version))
    args = parser.parse_args()

    if not utilities.MiscHelpers.checkArgumentValidity(parser, args):
        exit(1)

    if not os.path.exists(globals.LEPUS_INI_LOCATION): # if the file doesn't exist
        print(f"Warning: Couldn't find a lepus.ini, creating file in {globals.LEPUS_INI_LOCATION}...")
        command = f'printf "{LEPUS_BLANK_INI}" > {globals.LEPUS_INI_LOCATION}'
        os.system(command)


    printBanner()
    db = utilities.DatabaseHelpers.init()

    if args.doFlush:
        utilities.MiscHelpers.purgeOldFindings(db, args.domain)
        print("{0} {1} {2}".format(colored("\n[*]-Flushed", "yellow"), colored(args.domain, "cyan"), colored("from the database", "yellow")))
        exit(0)

    print("{0} {1}".format(colored("\n[*]-Running against:", "yellow"), colored(args.domain, "cyan")))

    old_resolved, old_unresolved, old_takeovers = utilities.MiscHelpers.loadOldFindings(db, args.domain)
    utilities.MiscHelpers.purgeOldFindings(db, args.domain)

    try:
        utilities.ScanHelpers.retrieveDNSRecords(db, args.domain)

        if args.zoneTransfer:
            zt_subdomains = utilities.ScanHelpers.zoneTransfer(db, args.domain)

        else:
            zt_subdomains = None

        if args.noCollectors:
            collector_subdomains = None

        else:
            print()
            collector_subdomains = []
            collector_subdomains += collectors.Censys.init(args.domain)
            collector_subdomains += collectors.CertSpotter.init(args.domain)
            collector_subdomains += collectors.CRT.init(args.domain)
            collector_subdomains += collectors.DNSTrails.init(args.domain)
            collector_subdomains += collectors.FOFA.init(args.domain)
            collector_subdomains += collectors.GoogleTransparency.init(args.domain)
            collector_subdomains += collectors.HackerTarget.init(args.domain)
            collector_subdomains += collectors.PassiveTotal.init(args.domain)
            collector_subdomains += collectors.PDChaos.init(args.domain)
            collector_subdomains += collectors.ProjectCrobat.init(args.domain, args.ranges)
            collector_subdomains += collectors.ProjectSonar.init(args.domain)
            collector_subdomains += collectors.Riddler.init(args.domain)
            collector_subdomains += collectors.Shodan.init(args.domain)
            collector_subdomains += collectors.Spyse.init(args.domain)
            collector_subdomains += collectors.ThreatCrowd.init(args.domain)
            collector_subdomains += collectors.ThreatMiner.init(args.domain)
            collector_subdomains += collectors.VirusTotal.init(args.domain)
            collector_subdomains += collectors.WaybackMachine.init(args.domain)
            collector_subdomains += collectors.ZoomEye.init(args.domain)

        if args.wordlist:
            wordlist_subdomains = utilities.MiscHelpers.loadWordlist(args.domain, args.wordlist)

        else:
            wordlist_subdomains = None

        findings = utilities.MiscHelpers.cleanupFindings(args.domain, old_resolved, old_unresolved, zt_subdomains, collector_subdomains, wordlist_subdomains)

        del old_unresolved
        del zt_subdomains
        del collector_subdomains
        del wordlist_subdomains
        collect()

        if findings:
            utilities.ScanHelpers.identifyWildcards(db, findings, args.domain, args.threads)
            utilities.ScanHelpers.massResolve(db, findings, args.domain, args.hideWildcards, args.threads)

            del findings
            collect()

            if args.permutate:
                submodules.Permutations.init(db, args.domain, args.permutation_wordlist, args.hideWildcards, args.threads)

            if args.reverse:
                submodules.ReverseLookups.init(db, args.domain, args.ripe, args.ranges, args.only_ranges, args.threads)

            if args.markovify:
                submodules.Markov.init(db, args.domain, args.markov_state, args.markov_length, args.markov_quantity, args.hideWildcards, args.threads)

            utilities.ScanHelpers.massRDAP(db, args.domain, args.threads)

            if args.portscan:
                submodules.PortScan.init(db, args.domain, args.ports, args.threads)

            if args.takeover:
                submodules.TakeOver.init(db, args.domain, old_takeovers, args.threads)

        utilities.MiscHelpers.exportFindings(db, args.domain, old_resolved, False)

    except KeyboardInterrupt:
        print(colored("\n[*]-Received keyboard interrupt! Shutting down...", "red"))
        utilities.MiscHelpers.exportFindings(db, args.domain, old_resolved, True)
        exit(-1)


if __name__ == "__main__":
    main()
