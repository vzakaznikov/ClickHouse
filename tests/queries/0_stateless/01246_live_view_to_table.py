#!/usr/bin/env python
import os
import sys
import time
import signal

CURDIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURDIR, 'helpers'))

from client import client, prompt, end_of_block

log = None
# uncomment the line below for debugging
#log=sys.stdout

with client(name='client1>', log=log) as client1, client(name='client2>', log=log) as client2:
    client1.expect(prompt)
    client2.expect(prompt)

    client1.send('SET allow_experimental_live_view = 1')
    client1.expect(prompt)

    client1.send('DROP TABLE IF EXISTS test.lv')
    client1.expect(prompt)
    client1.send('DROP TABLE IF EXISTS test.mt')
    client1.expect(prompt)
    client1.send('DROP TABLE IF EXISTS test.sums')
    client1.expect(prompt)
    client1.send('CREATE TABLE test.mt (a Int32) Engine=MergeTree order by tuple()')
    client1.expect(prompt)
    client1.send('CREATE TABLE test.sums (s Int64, _version UInt64) Engine=MergeTree ORDER BY tuple()')
    client1.expect(prompt)
    client1.send('CREATE LIVE VIEW test.lv TO test.sums AS SELECT sum(a) AS s FROM test.mt')
    client1.expect(prompt)

    client2.send('SELECT * FROM test.sums ORDER BY _version DESC LIMIT 1 FORMAT CSV')
    client2.expect('0,1\r\n')
    client2.expect(prompt)

    client2.send('INSERT INTO test.mt VALUES (1),(2),(3)')
    client2.expect(prompt)
    time.sleep(0.25)
    client2.send('SELECT * FROM test.sums ORDER BY _version DESC LIMIT 1 FORMAT CSV')
    client2.expect('6,2\r\n')
    client2.expect(prompt)

    client2.send('INSERT INTO test.mt VALUES (4),(5),(6)')
    client2.expect(prompt)
    time.sleep(0.25)
    client2.send('SELECT * FROM test.sums ORDER BY _version DESC LIMIT 1 FORMAT CSV')
    client2.expect('21,3\r\n')
    client2.expect(prompt)

    client1.send('DROP TABLE test.lv')
    client1.expect(prompt)
    client1.send('DROP TABLE test.sums')
    client1.expect(prompt)
    client1.send('DROP TABLE test.mt')
    client1.expect(prompt)
