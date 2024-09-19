from equation_database import isbn_9780511628788 as book
# import equation_database.isbn_9780511628788 as book


def test_table_7_1():
    assert book.table_7_1_qqp_qqp().equals(book.table_7_1_qqpb_qqpb())

    assert book.table_7_1_qqb_qpqpb().equals(
        book.table_7_1_qqpb_qqpb().subs(
            {"s": "t", "t": "s"}, simultaneous=True, all=True
        )
    )

    assert book.table_7_1_qq_qq().equals(
        book.table_7_1_qqb_qqb().subs({"u": "s", "s": "u"}, simultaneous=True, all=True)
    )
