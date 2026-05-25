from lib.lists import LinkedList


def test_linked_list():
    ll = LinkedList(14)
    assert ll.as_list() == [14]
    assert ll.head.data == 14
    assert ll.tail.data == 14

    ll.append(2)
    assert ll.as_list() == [14, 2]
    assert ll.head.data == 14
    assert ll.tail.data == 2

    ll.append(20)
    assert ll.as_list() == [14, 2, 20]

    ll.prepend(31)
    assert ll.as_list() == [31, 14, 2, 20]

    _ = ll.insert_after(2, 16)
    assert ll.as_list() == [31, 14, 2, 16, 20]

    _ = ll.insert_after(20, 55)
    assert ll.as_list() == [31, 14, 2, 16, 20, 55]

    _ = ll.remove(55)
    assert ll.as_list() == [31, 14, 2, 16, 20]

    _ = ll.remove(31)
    assert ll.as_list() == [14, 2, 16, 20]

    ll.prepend(67)
    assert ll.as_list() == [67, 14, 2, 16, 20]

    _ = ll.insert_after(20, 58)
    assert ll.as_list() == [67, 14, 2, 16, 20, 58]

    ll.append(89)
    assert ll.as_list() == [67, 14, 2, 16, 20, 58, 89]
