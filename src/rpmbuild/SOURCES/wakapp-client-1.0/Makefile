wakapp-client:
	gcc -o wakapp-client wakapp-client.c

clean:
	rm wakapp-client

install:
	mkdir -p $(DESTDIR)/usr/bin
	install -m 0755 wakapp-client $(DESTDIR)/usr/bin/wakapp-client
